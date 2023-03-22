import socket
import threading
from tkinter import *
from database import *
from classes.gui import *
import mysql.connector

def receive():
    while True:
        if app.status == 2:
            message = app.client.recv(2048).decode('utf-8')
            print(message)
            Label(app.chat_frame, text=message).pack()

app = Interface()
receive_thread = threading.Thread(target=receive)
receive_thread.start()
app.run()
cursor.close()