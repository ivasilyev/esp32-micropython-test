from utils import Utils
try:
    import usocket as socket
except ImportError:
    import socket
from utime import sleep
from utils import Utils
from gc import collect


class HTTPServer:
    HOST = "0.0.0.0"
    PORT = 80
    TYPE_HTML = "text/html; charset=utf-8"

    def __init__(self):
        self.is_enabled = True
        self.addr = socket.getaddrinfo(self.HOST, self.PORT)[0][-1]
        self.socket = None
        self.routes = dict()
        self._html_template = Utils.load_string("index.html")
        self._css_template = Utils.load_string("styles.css")
        self._js_template = Utils.load_string("main.js")
        try:
            self.create_socket()
        except OSError:
            print("A socket is still opened, restarting...")
            Utils.hard_reset()

    def update_route(self, path, func):
        if path not in self.routes:
            self.routes[path] = func

    def create_socket(self):
        if not self.socket:
            self.socket = socket.socket()
            self.socket.bind(self.addr)
            self.socket.settimeout(2)
            self.socket.listen(5)
            self.socket.setblocking(False)
            print("Listening on: {}".format(self.addr))

    @staticmethod
    def is_request_contains(request: bytes, target: str):
        """
        Sample content:
        b'GET /?nowhere HTTP/1.1\r\n
        Host: <host ip-address>\r\n
        User-Agent: <user-agent>\r\n
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n
        Accept-Language: en-US,en;q=0.5\r\n
        Accept-Encoding: gzip, deflate\r\n
        Referer: http://<host ip-address>/?nowhere\r\n
        Connection: keep-alive\r\n
        Upgrade-Insecure-Requests: 1\r\n\
        r\n'
        """
        return str(request).find(target) > 0

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
        conn.send(payload)

    def handle_http(self, conn):
        data = b""
        while b"\r\n" not in data:
            request = conn.recv(1024)
            if not request:
                break
            else:
                data += request
            if not data:
                return
            udata = data.decode("utf-8")
            udata = udata.split("\r\n", 1)[0]
            method, string, protocol = udata.split(" ", 2)
            address = string
            params = dict()
            if string.find('?') != -1:
                address = string.split('?')[0]
                params = dict(i.split('=') for i in string.split('?')[1].split('&'))
            if method != "GET":
                self.send_response(conn, status="404 Not Found", payload="Page not found")
                return
            if len(params) > 0:
                print(params)
                # self.send_response(conn, type_=self.TYPE_HTML, payload=self.render())
            self.send_response(conn, type_=self.TYPE_HTML, payload=self.render())

    def response(self):
        try:
            connection, self.addr = self.socket.accept()
            print('client connected from', self.addr)
        except:
            return
        try:
            # request = connection.recv(1024)
            # response = self.render()
            # if self.is_request_contains(request, "/?nowhere"):
            #     print("The way is lost!")
            #     response = response.replace('<button class="button">',
            #                                 '<button class="button" disabled>')
            # connection.send(b"HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
            # connection.send(response)
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
        finally:
            self.socket.close()
            collect()
