from utils import Utils
try:
    import usocket as socket
except ImportError:
    import socket


class HTTPServer:
    def __init__(self):
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.socket = socket.socket()
        self.socket.bind(self.addr)
        self.socket.listen(1)
        self._html_template = Utils.load_string("index.html")
        self._css_template = Utils.load_string("styles.css")
        print("Listening on: {}".format(self.addr))

    def render(self):
        # I miss React ;_;
        return self._html_template.format(
            BUTTON="A button"
        ).replace("<style></style>", "<style>" + self._css_template + "</style>")

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

    def response(self):
        connection, self.addr = self.socket.accept()
        print('client connected from', self.addr)
        request = connection.recv(1024)
        response = self.render()
        if self.is_request_contains(request, "/?nowhere"):
            print("The way is lost!")
            response = response.replace('<button class="button">',
                                        '<button class="button" disabled>')
        connection.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        connection.send(response)
        connection.close()
