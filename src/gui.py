from tkinter import *
import database
import server


class Interface:
    def __init__(self):
        self.root = Tk()
        self.root.title("Discord")
        self.root.geometry("650x500")

    def buttons(self):
        self.connexion = Button(text="Se Connecter")
        self.connexion.pack()

    def run(self):
        self.buttons()
        self.root.mainloop()



app = Interface()
app.run()
    