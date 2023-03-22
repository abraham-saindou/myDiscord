import socket
import threading
import thread


class Server:
    def __init__(self):
        self.localhost = "127.0.0.1"
        self.host = "10.10.15.89"
        self.port = 65432
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind((self.localhost, self.port))

    def incoming_connections(self):
        self.soc.listen(10)
        print("Le serveur est en attente de connexion...")
        conn, addr = self.soc.accept()
        print(f"Un client vient de se connecter")
        mythread = thread.ThreadForClient(conn)
        mythread.start()
        conn.close()
        self.close_server()

    def close_server(self):
        self.soc.close()


server1 = Server()
server1.daemon = True
server1.incoming_connections()

