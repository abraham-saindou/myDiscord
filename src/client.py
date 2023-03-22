import time
import socket
import threading
from tkinter import *
from classes.gui import *
import mysql.connector

HOST ='127.0.0.1'
PORT = 33000

db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "SuperP3scado",
        database = "Boutique"
)

def receive():
    while True:
        if app.status == 1:
            message = client.recv(2048).decode('utf-8')
            Label(app.chat_frame, text=message).pack()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))  
print('Connected succesfully.')


app = Interface(client)
receive_thread = threading.Thread(target=receive)
receive_thread.start()
app.run()