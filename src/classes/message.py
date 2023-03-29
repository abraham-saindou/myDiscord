from tkinter import *
from database import *

class Messages:
    def __init__(self, author, date, content, channel, destination = ""):
        self.author = author
        self.destination = destination
        self.content = content
        self.channel = channel
        self.date = date

    def ajouter(self):

        if self.channel == 1:
            cursor.execute("INSERT INTO Messages (id_auteur, date_pub, texte, id_canal, id_destinataire)\
                        VALUES (?,?,?,?,?)", [self.author, self.date, self.content, self.channel, self.destination])
        else:
            cursor.execute("INSERT INTO Messages (id_auteur, date_pub, texte, id_canal)\
                        VALUES (?,?,?,?)", [self.author, self.date, self.content, self.channel])
        db.commit()

    def display(self, surface):

        Label(surface, text=self.content, anchor="nw").pack(fill=X)