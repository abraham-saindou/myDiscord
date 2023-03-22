import socket
import threading

HOST = '127.0.0.1'
PORT = 33000
clients = {}
addresses = {}

def incoming_connection():

    while True:
        client, address = server.accept()
        print(f"{address[0]} est connecté")
        addresses[client] = address
        threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(client):

    name = client.recv(2048).decode("utf8")
    welcome = "Welcome %s!" %name
    client.send(bytes(welcome, "utf8"))
    message = "%s has joined." %name
    broadcast(bytes(message, "utf8"))
    clients[client] = name

    while True:
        message = client.recv(2048)
        if message != bytes("{quit}", "utf8"):
            broadcast(message, name+": ")
        else:
            client.close()
            del clients[client]
            broadcast(bytes("%s has left." %name, "utf8"))
            break

def broadcast(message, sender=""):
    for user in clients:
        user.send(bytes(sender, "utf8")+message)
        

def main():
    server.listen(5)
    accept_client = threading.Thread(target=incoming_connection)
    accept_client.start()
    accept_client.join()
    server.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
main()