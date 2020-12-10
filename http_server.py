from utils import Utils
try:
    import usocket as socket
except ImportError:
    import socket
from utime import sleep
from utils import Utils
from gc import collect
from json import loads
from demo import AnimationController, ColorManager


class HTTPServer:
    HOST = "0.0.0.0"
    PORT = 80
    TYPE_HTML = "text/html; charset=utf-8"
    BUFFER_SIZE = 1024

    def __init__(self, controller: AnimationController):
        self.is_enabled = True
        self._controller = controller
        self.addr = socket.getaddrinfo(self.HOST, self.PORT)[0][-1]
        self.socket = None
        self.routes = dict()
        self._html_template = Utils.load_string("index.html")
        self._css_template = Utils.load_string("styles.css")
        self._js_template = Utils.load_string("main.js")
        try:
            self.start()
        except OSError:
            print("A socket is still opened, restarting...")
            self.restart()

    def start(self):
        self.is_enabled = True
        if not self.socket:
            self.socket = socket.socket()
            self.socket.bind(self.addr)
            self.socket.settimeout(2)
            self.socket.listen(5)
            self.socket.setblocking(False)
            print("The HTTP server is listening on: {}".format(self.addr))

    def stop(self):
        if self.is_enabled:
            self.is_enabled = False
            print("Stop the web server")
            self.socket.close()
            self.socket = None

    def restart(self):
        self.stop()
        sleep(1)
        try:
            self.start()
        except OSError:  # EADDRINUSE
            Utils.hard_reset()

    def update_route(self, path, func):
        if path not in self.routes:
            self.routes[path] = func

    @staticmethod
    def is_request_contains(request: bytes, target: str):
        return request.decode("utf-8").find(target) > 0

    def render(self):
        # I miss React ;_;
        out = self._html_template.format(
            BUTTON="A button"
        )
        out = out.replace('<link rel="stylesheet" type="text/css" href="./styles.css">',
                          "<style>" + self._css_template + "</style>")
        out = out.replace('<script src="./main.js"></script>',
                          "<script>" + self._js_template + "</script>")
        return out

    @staticmethod
    def send(connection, b: bytes):
        try:
            connection.send(b)
        except OSError:
            Utils.hard_reset()

    def send_response(self, conn, status="200 OK", type_="text/plain; charset=utf-8", payload=""):
        payload = payload.encode("utf-8")
        header_lines = ["HTTP/1.1 {}".format(status), "Server: ESP32", "Connection: close",
                        "Content-Type: {}".format(type_), "Content-Length: {}".format(len(payload)),
                        "", ""]
        self.send(conn, "\r\n".join(header_lines).encode("utf-8"))
        self.send(conn, payload)

    def handle_json(self, j):
        try:
            d = loads(Utils.parse_percent_encoding(j))
        except:
            return
        a = d["animation_name"]
        c = list({i: d["colors"][i] for i in sorted(d["colors"].keys())}.values())
        cc = ColorManager.create_color_loop([Utils.convert_hex_to_rgb(i) for i in c])
        params = str((a, cc))
        print(params)
        # self._controller.set_animation(a, colors=cc)
        _ = getattr(self._controller._animations, a)(colors=cc)

    def handle_http(self, conn):
        data = b""
        while b"\r\n" not in data:
            request = conn.recv(self.BUFFER_SIZE)
            if not request:
                break
            else:
                data += request
            if not data:
                return
        udata = data.decode("utf-8")
        udata = udata.split("\r\n", 1)[0]
        method, string, protocol = udata.split(" ", 2)
        path = string
        params = dict()
        if string.find('?') != -1:
            path = string.split('?')[0]
            params = dict(i.split('=') for i in string.split('?')[1].split('&'))
        if method != "GET":
            print("method")
            print(udata)
            if method in ["POST", "PUT"]:
                pass
            else:
                self.send_response(conn, status="404 Not Found", payload="404\r\nPage not found")
                return
        if len(params) > 0:
            print("params")
            print(params)
            if "data" in params.keys():
                self.handle_json(params["data"])
        self.send_response(conn, type_=self.TYPE_HTML, payload=self.render())

    def response(self):
        try:
            connection, self.addr = self.socket.accept()
            print("Client connected:", self.addr)
        except:
            return
        try:
            self.handle_http(connection)
        except:
            self.send_response(connection, "500 Internal Server Error", payload="Error")
            connection.close()
        finally:
            connection.close()

    def run(self):
        try:
            while self.is_enabled:
                self.response()
                collect()
        except:
            self.restart()
        finally:
            self.stop()
            collect()
