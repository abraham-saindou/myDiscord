import socket


class Client:
    def __init__(self):
        self.host = '10.10.15.89'  # The server's hostname or IP address
        self.localhost = '127.0.0.1'
        self.port = 65432        # The port used by the server
        self.client = socket.socket()
        # self.server.bind((self.localhost, self.port))

    def ask_connection(self):
        self.client.connect((self.localhost, self.port))
        print(f"Client connecté")
        self.client.send('Hello, world'.encode())
        data = self.client.recv(1024)

        print('Received', repr(data))

    def close_client(self):
        self.client.close()


user1 = Client()
user1.ask_connection()
user1.close_client()
