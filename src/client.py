import socket
import threading
from tkinter import *
import mysql.connector

HOST ='127.0.0.1'
PORT = 33000

def comm_server(client):
    nom = input("Entrer nom: ")
    if nom != '':
        client.sendall(nom.encode())
    else:
        print("le nom d'utilisateur ne peut pas etre vide")
        exit(0)

    threading.Thread(target=ecoute_messages_serveur, args=(client, )).start()
    envoi_message_serveur(client)

def ecoute_messages_serveur(client):
    
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            nom = message.split(':')[0]
            contenu = message.split(':')[1]

            print(f"\n{nom}: {contenu}")
        else:
            print('le message est vide')

def envoi_message_serveur(client):
    
    while True:

        message = input()

        if message != '':
            client.sendall(message.encode()) 
        else:
            print('message vide')
            exit(0)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))  
        print('Connexion réussie')
    except:
        print('impossible de se connecter au serveur')

    comm_server(client)
main()