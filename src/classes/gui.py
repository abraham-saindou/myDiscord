import socket
from tkinter import *
from classes.user import *

HOST ='127.0.0.1'
PORT = 33000

class Interface:
    def __init__(self):
        self.root = Tk()
        self.root.title("Discord")
        self.root.geometry("300x500")
        self.status = 0

    #Formulaire de connection
    def connect_form(self):

        self.input_email = Entry(self.root)
        self.input_password = Entry(self.root)

        self.input_email.pack()
        self.input_password.pack()
        Button(self.root, text="Connect", command=self.connect).pack()
        Button(self.root, text="Register", command=lambda: self.navigation(1)).pack()

    #Connection au serveur
    def connect(self):

        mail = self.input_email.get()
        pwd = self.input_password.get()

        self.user = User(mail, pwd)

        if self.user.connection():

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))  

            self.navigation(2)
            self.client.sendall(mail.encode())

    #Formulaire d'inscription
    def register_form(self):
        
        self.input_name = Entry(self.root)
        self.input_fname = Entry(self.root)
        self.input_email = Entry(self.root)
        self.input_password = Entry(self.root)

        self.input_name.pack()
        self.input_fname.pack()
        self.input_email.pack()
        self.input_password.pack()
        Button(self.root, text="Register", command=self.register).pack()

    #Inscription
    def register(self):

        name = self.input_name.get()
        fname = self.input_fname.get()
        mail = self.input_email.get()
        pwd = self.input_password.get()

        self.user = User(mail, pwd, name, fname)

        if self.user.register():
            self.navigation(0)


    def chatroom(self):

        self.chat_frame = Frame(self.root)
        self.input_message = Entry(self.root)

        self.chat_frame.grid(row=0, column=0, columnspan=2)
        self.input_message.grid(row=1, column=0, columnspan=2)

        Button(self.root, text="Send", command=self.send).grid(row=2, column=0)
        Button(self.root, text="Quit", command=self.disconnect).grid(row=2, column=1)

    #Envoi de message au serveur
    def send(self):

        message = self.input_message.get()

        if message == "{quit}":
            self.disconnect()
        elif message != '':
            self.client.sendall(message.encode()) 
                
    def disconnect(self):
        message = "{quit}"
        self.client.sendall(message.encode())
        self.client.close()
        self.navigation(0)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    #Changement de page
    def navigation(self, page):

        self.status = page
        self.clear()
        match self.status:
            case 0:
                self.connect_form()
            case 1:
                self.register_form()
            case 2:
                self.chatroom()

    def run(self):
        self.navigation(0)
        self.root.mainloop()

    