from tkinter import *
from classes.user import *
import database

class Interface:
    def __init__(self, client, db):
        self.root = Tk()
        self.root.title("Discord")
        self.root.geometry("650x500")
        self.client = client

        self.status = 0

    def connect(self):
        self.status = 1
        self.navigation()

    def send(self):

        message = self.input_message.get()

        if message == "{quit}":
            self.quit()
        elif message != '':
            self.client.sendall(message.encode()) 
                
    def quit(self):
        message = "{quit}"
        self.client.sendall(message.encode())
        self.client.close()
        self.root.quit()

    def connect_form(self):

        self.input_email = Entry(self.root)
        self.input_password = Entry(self.root)

        self.input_email.pack()
        self.input_password.pack()
        Button(self.root, text="Connect", command=self.connect).pack()

    def chatroom(self):

        self.chat_frame = Frame(self.root)
        self.input_message = Entry(self.root)

        self.chat_frame.grid(row=0, column=0, columnspan=2)
        self.input_message.grid(row=1, column=0, columnspan=2)

        Button(self.root, text="Send", command=self.send).grid(row=2, column=0)
        Button(self.root, text="Quit", command=self.quit).grid(row=2, column=1)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def navigation(self):
        self.clear()
        match self.status:
            case 0:
                self.connect_form()
            case 1:
                self.chatroom()

    def run(self):
        self.navigation()
        self.root.mainloop()

    