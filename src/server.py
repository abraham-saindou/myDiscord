import socket
import threading

HOST = '127.0.0.1'
PORT = 33000
clients = []

def gestion_client(client):

    while True:
        nom = client.recv(2048).decode('utf-8')
        if nom != '':
            clients.append((nom, client))
            break
        else:
            print('le nom du client est vide')

    threading.Thread(target=ecoute_messages_client, args=(client, nom)).start()

def ecoute_messages_client(client, nom):
    
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            texte = nom + ':' +  message
            envoi_general(texte)
        else:
            print(f'le message de {nom} est vide')

def envoi(client ,message):
    client.sendall(message.encode())


def envoi_general(message):
    for user in clients:
        envoi(user[1], message)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print("Serveur en marche.")
    except:
        print('hôte introuvable')

    server.listen(5)

    while True:
        client, address = server.accept()
        print(f"{address[0]} est connecté")

        threading.Thread(target=gestion_client, args=(client,)).start()

main()