import socket


class Client:
    def __init__(self):
        self.host = '10.10.15.89'  # The server's hostname or IP address
        self.port = 65432        # The port used by the server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.host, self.port6)

    def ask_connection(self):
        while True:
            self.server.connect((self.host, self.port))
            self.server.sendall(b'Hello, world')
            data = self.server.recv(1024)

            print('Received', repr(data))