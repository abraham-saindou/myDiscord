import socket
import threading
from classes.message import *
from database import *
import datetime


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

            date = datetime.datetime.now()
            author_id = get_user_id(name.split(" ")[0], name.split(" ")[1])

            #Messages Privés
            if message[:2] == bytes("/p", "utf8"):

                dest =  message[2:].decode("utf-8").split(":")[0]
                content = message[2:].decode("utf-8").split(":")[1]
                get_client(dest).send(bytes(f"({date}) {name}: {content}", "utf8"))

                dest_id = get_user_id(dest.split(" ")[0], dest.split(" ")[1])
                Messages(author_id, date, content, 2, dest_id).add()

            #Messages Publics
            else:

                channel = message.decode("utf-8").split(":")[0]
                content = message.decode("utf-8").split(":")[1]

                broadcast(content, int(channel), name, date, author_id)
        else:
            client.close()
            del clients[client]
            broadcast(bytes("%s has left." %name, "utf8"))
            break

def broadcast(message, channel = 0, sender="", date = "", id = "" ):

    if id != "":
        Messages(id, date, message, channel).add()

    for user in clients:
        if sender != "":
            user.send(bytes(f"{channel}({date}) {sender}: {message}", "utf8"))
        else:
            user.send(message)

def get_client(name):
    for client in clients:
        if clients[client] == name:
            return client
        

def main():
    server.listen(5)
    accept_client = threading.Thread(target=incoming_connection)
    accept_client.start()
    accept_client.join()
    server.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
main()