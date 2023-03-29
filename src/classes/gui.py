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
        self.root.geometry("400x500")
        self.destination = "test test"
        self.channel = 0
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

        self.connect_frame.place(relx=.5, rely=.5, anchor=CENTER)

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

            self.root.title(f"Discord - {self.user.firstname} {self.user.lastname}")
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
        
        self.register_frame.place(relx=.5, rely=.5, anchor=CENTER)

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
        self.settings_frame = Frame(self.root)
        self.input_message = Entry(self.entry_frame)
        Scrollbar(self.chat_frame).pack(side=RIGHT, fill=Y)
        Button(self.settings_frame, command= self.change_channel, text="Change channel", width=35).pack(side=LEFT, expand=True)

        if self.channel == 1:
            users = get_users()
            self.filter = StringVar()
            self.filter.set(self.destination)
            OptionMenu(self.settings_frame, self.filter, *users, command= self.change_user).pack(side=RIGHT, expand=True)
        
        self.settings_frame.pack()
        self.chat_frame.pack_propagate(0)
        self.chat_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.entry_frame.pack(side=BOTTOM, fill=X)
        self.input_message.pack(fill=X, expand=True)

        Button(self.entry_frame, text="Send", command=self.send, width=20).pack(side=RIGHT, expand=True)
        Button(self.entry_frame, text="Log out", command=self.disconnect, width=20).pack(side=LEFT, expand=True)

        match self.channel:
            case 0:
                messages = get_public_messages()
            case 1:
                dest_id = get_user_id(self.destination.split(" ")[0], self.destination.split(" ")[1])

                messages = get_private_messages(self.user.id, dest_id)

        if messages:    
            for message in messages:
                message.display(self.chat_frame)

    def receive(self):

        while True:
            message = self.client.recv(2048).decode('utf-8')
            if message[:2] == "/p":
                if self.channel == 1:
                    Label(self.chat_frame, text=message[2:], anchor="nw").pack(fill=X)
            else:
                Label(self.chat_frame, text=message, anchor="nw").pack(fill=X)

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

    def change_channel(self):
        if self.channel == 0:
            self.channel = 1
        else:
            self.channel = 0

        self.navigation(2)
    
    def change_user(self, user):

        self.destination = self.filter.get()
        self.navigation(2)
                
    def disconnect(self):
        message = "{quit}"
        self.client.sendall(message.encode())
        self.client.close()
        self.root.title("Discord")
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

    