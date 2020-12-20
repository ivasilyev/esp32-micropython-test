try:
    import usocket as socket
except ImportError:
    import socket

from utime import sleep_ms
from gc import collect
from json import loads, dumps
from collections import OrderedDict
from utils import Utils
from demo import AnimationController, ColorManager


class HTTPServer:
    HOST = "0.0.0.0"
    PORT = 80
    TYPE_HTML = "text/html; charset=utf-8"
    BUFFER_SIZE = 1024

    def __init__(self, controller: AnimationController):
        self.is_enabled = False
        self._controller = controller
        self._animation_params = ""
        self.addr = socket.getaddrinfo(self.HOST, self.PORT)[0][-1]
        self.socket = None
        self.routes = dict()

        self._html_template = Utils.load_string("index.html")
        self._css_template = Utils.load_string("styles.css")
        self._js_template = Utils.load_string("main.js")

        self.state = {}
        self.start()

    def start(self):
        self.is_enabled = True
        print("Start the web server")
        try:
            self.socket = socket.socket()
            self.socket.bind(self.addr)
        except OSError as e:
            if e.args[0] == 98:  # EADDRINUSE
                print("A socket is still opened, restarting...")
                Utils.hard_reset()
        self.socket.settimeout(2)
        self.socket.listen(5)
        self.socket.setblocking(False)
        sleep_ms(100)
        print("The HTTP server is listening on: {}".format(self.addr))

    def stop(self):
        if self.is_enabled:
            self.is_enabled = False
            print("Stop the web server")
            self.socket.close()

    def restart(self):
        self.stop()
        sleep_ms(100)
        self.start()

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
    def send_response(conn, status="200 OK", type_="text/plain; charset=utf-8", payload=""):
        payload = payload.encode("utf-8")
        header_lines = ["HTTP/1.1 {}".format(status), "Server: ESP32", "Connection: close",
                        "Content-Type: {}".format(type_), "Content-Length: {}".format(len(payload)),
                        "", ""]
        conn.send("\r\n".join(header_lines).encode("utf-8"))
        conn.sendall(payload)

    def send_current_state(self):
        pass

    def receive_submission(self, j):
        try:
            d = loads(Utils.parse_percent_encoding(j))
        except:
            return
        self.state.update(d)
        kwargs = dict()
        if "colors" in d.keys():
            self.state["colors"] = OrderedDict(sorted(d["colors"].items()))
            colors = [ColorManager.convert_hex_to_rgb(i) for i in self.state["colors"].values()]
            kwargs["colors"] = ColorManager.create_color_loop(
                colors, steps=self.state["color_transitions"])
            if self.state["always_lit"]:
                kwargs["always_lit"] = self.state["always_lit"]
            if self.state["pause"]:
                kwargs["pause"] = self.state["pause"]
            self._controller.set_animation(self.state["animation"], **kwargs)

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
        method, payload, protocol = udata.split(" ", 2)
        path = payload
        params = dict()
        if payload.find('?') != -1:
            path = payload.split('?')[0]
            try:
                params = dict(i.split('=') for i in payload.split('?')[1].split('&'))
            except:
                print("payload", payload)
                return
        print("udata", udata)
        print(method, payload, protocol)
        if method != "GET":
            if method in ["POST", "PUT"]:
                self.send_response(conn, type_=self.TYPE_HTML, payload=self.render())
            else:
                self.send_response(conn, status="404 Not Found", payload="404\r\nPage not found")
                return
        if len(params) > 0:
            print("params", params)
            if "data" in params.keys():
                self.receive_submission(params["data"])
                self.send_response(conn, type_="application/json", payload=dumps(self.state))
        if path == "/":
            self.send_response(conn, type_=self.TYPE_HTML, payload=self.render())
        if "state" in path:
            self.send_response(conn, type_="application/json", payload=dumps(self.state))

    def response(self):
        try:
            connection, self.addr = self.socket.accept()
            print("Client connected:", self.addr)
            try:
                self.handle_http(connection)
            except OSError as e:
                if e.args[0] == 104:  # ECONNRESET
                    print("Connection reset:", e)
                    connection.close()
            except Exception as e:
                print("Connection handling problem:", e)
                self.send_response(connection, "500 Internal Server Error", payload="Error")
                connection.close()
                raise
            finally:
                connection.close()
        except OSError as e:
            if e.args[0] == 11:  # EAGAIN
                sleep_ms(100)

    def run(self):
        while True:
            try:
                self.response()
                collect()
            except Exception as e:
                print(e)
                sleep_ms(2000)
                raise
