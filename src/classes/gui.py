import socket
import threading
from tkinter import *
from classes.user import *
from tkinter.messagebox import *

HOST ='127.0.0.1'
PORT = 33000

class Interface:
    def __init__(self):
        self.root = Tk()
        self.root.title("Discord")
        self.root.geometry("300x500")
        self.channel = 0
        self.destination = ""
        self.status = 0

    #Formulaire de connection
    def connect_form(self):

        self.connect_frame = Frame(self.root)

        self.input_email = Entry(self.connect_frame)
        self.input_password = Entry(self.connect_frame, show="*")

        Label(self.connect_frame, text="E-mail").grid(row=0,column=0)
        self.input_email.grid(row=0, column=1)
        Label(self.connect_frame, text="Password").grid(row=1, column=0)
        self.input_password.grid(row=1, column=1)

        Button(self.connect_frame, text="Connect", command=self.connect, width=25).grid(row=2, columnspan=2, pady=3)
        Button(self.connect_frame, text="Register", command=lambda: self.navigation(1), width=25).grid(row=3, columnspan=2)

        self.connect_frame.pack(pady=100)

    #Connection au serveur
    def connect(self):

        mail = self.input_email.get()
        pwd = self.input_password.get()

        self.user = User(mail, pwd)

        if self.user.connection():

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((HOST, PORT))
            
            receive_thread = threading.Thread(target=self.receive)
            receive_thread.start()  

            self.navigation(2)
            self.client.sendall(f"{self.user.lastname} {self.user.firstname}".encode())
        else:
            showerror('Connection', 'Incorrect email or password')

    #Formulaire d'inscription
    def register_form(self):

        self.register_frame = Frame(self.root)
        
        self.input_name = Entry(self.register_frame)
        self.input_fname = Entry(self.register_frame)
        self.input_email = Entry(self.register_frame)
        self.input_password = Entry(self.register_frame, show="*")

        Label(self.register_frame, text="Last name").grid(row=0,column=0)
        self.input_name.grid(row=0,column=1)
        Label(self.register_frame, text="First name").grid(row=1,column=0)
        self.input_fname.grid(row=1,column=1)
        Label(self.register_frame, text="E-mail").grid(row=2,column=0)
        self.input_email.grid(row=2,column=1)
        Label(self.register_frame, text="Password").grid(row=3,column=0)
        self.input_password.grid(row=3,column=1)

        Button(self.register_frame, text="Register", command=self.register, width=25).grid(row=4,columnspan=2, pady=3)
        Button(self.root, text="Log in", command=lambda: self.navigation(0)).pack(side=BOTTOM, anchor="e")
        
        self.register_frame.pack(pady=100)

    #Inscription
    def register(self):

        name = self.input_name.get()
        fname = self.input_fname.get()
        mail = self.input_email.get()
        pwd = self.input_password.get()

        self.user = User(mail, pwd, name, fname)

        if self.user.register():
            self.navigation(0)
        else:
            showerror('Register', 'Email already used')


    def chatroom(self):

        self.chat_frame = Frame(self.root)
        self.entry_frame = Frame(self.root)
        self.input_message = Entry(self.entry_frame)
        self.message_list = Listbox(self.chat_frame)
        Scrollbar(self.message_list).pack(side=RIGHT, fill=Y)
        
        self.chat_frame.pack_propagate(0)
        self.chat_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.message_list.pack(fill=BOTH, expand=True)
        self.entry_frame.pack(side=BOTTOM, fill=X)
        self.input_message.pack(fill=X, expand=True)

        Button(self.entry_frame, text="Send", command=self.send, width=20).pack(side=RIGHT, expand=True)
        Button(self.entry_frame, text="Log out", command=self.disconnect, width=20).pack(side=LEFT, expand=True)

        match self.channel:
            case 0:
                messages = get_public_messages()
            case 1:
                dest_id = get_user_id(self.destination.split(" ")[0], self.destination.split(" ")[0])
                message = get_private_messages(self.user.id, dest_id)
                
        for message in messages:
            message.display(self.message_list)

    def receive(self):

        while True:
            message = self.client.recv(2048).decode('utf-8')
            self.message_list.insert(END, message)

    #Envoi de message au serveur
    def send(self):

        message = self.input_message.get()

        if message == "{quit}":
            self.disconnect()

        elif message != '':
            if self.channel != 1:
                self.client.sendall(message.encode())
            else:
                self.client.sendall((f"/p{self.destination}:{message}").encode())
                
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

    