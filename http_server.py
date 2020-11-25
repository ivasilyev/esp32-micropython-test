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

    def response(self):
        connection, self.addr = self.socket.accept()
        print('client connected from', self.addr)
        request = connection.recv(1024)
        response = self.render()
        connection.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        connection.send(response)
        connection.close()
