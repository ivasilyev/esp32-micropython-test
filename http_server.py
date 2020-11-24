try:
    import usocket as socket
except ImportError:
    import socket
# from machine import Pin

HTML = """<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <title>Hello!</title>
    </head>

    <body>
        <h1>Hello World!</h1>
        <p>This is a simple paragraph.</p>
    </body>

</html>"""


class HTTPServer:
    def __init__(self):
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.socket = socket.socket()
        self.socket.bind(self.addr)
        self.socket.listen(1)
        print("Listening on: {}".format(self.addr))

    def response(self):
        cl, self.addr = self.socket.accept()
        print('client connected from', self.addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        response = HTML
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
