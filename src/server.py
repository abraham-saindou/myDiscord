import socket


class Server:
    def __init__(self):
        self.localhost = "127.0.0.1"
        self.host = "10.10.15.89"
        self.port = 65432
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(self.host, self.port)

    def incoming_connections(self):
        while True:
            self.soc.listen(10)
            print("Le serveur est en attente de connexion...")
            conn, addr = self.soc.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
