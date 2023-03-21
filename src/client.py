import time
import socket
import threading
from tkinter import *
import mysql.connector
from classes.user import *

HOST ='127.0.0.1'
PORT = 33000

db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "Boutique"
)

def receive():
    
    while True:
        message = client.recv(2048).decode('utf-8')
        print(message)

def send():

    message = input_message.get()

    if message == "{quit}":
        quit()
    elif message != '':
        client.sendall(message.encode()) 
            

def quit():
    message = "{quit}"
    client.sendall(message.encode())
    client.close()
    fenetre.quit()

fenetre = Tk()
fenetre.geometry("300x600")

input_message = Entry(fenetre)
input_message.grid(row=1, column=0, columnspan=2)
btn_send = Button(fenetre, text="Send", command=send).grid(row=2, column=0)
btn_quit = Button(fenetre, text="Quit", command=quit).grid(row=2, column=1)



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))  
print('Connected succesfully.')

receive_thread = threading.Thread(target=receive)
receive_thread.start()
fenetre.mainloop()
