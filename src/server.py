import socket


class Sock:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 65432
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(self.host, self.port)

    def incoming_connections(self):
        while True:
            self.soc.listen(10)
            print("Le serveur est en attente de connexion...")
