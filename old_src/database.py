import mysql.connector
import time


class SQL:
    def __init__(self, hote, utilisateur, mdp, database):
        self.connector = mysql.connector.connect()
        self.cursor = self.connector.cursor()

    def new_user(self, nom, prenom, mail, mdp):
        insert = "INSERT INTO utilsateurs(nom, prenom, email, mdp)"
        self.cursor.execute(insert, [nom, prenom, mail, mdp])

    def add_message(self, id_auteur, date_pub, texte):
        message = "INSERT INTO messages(id_auteur, date_pub, texte)"
        self.cursor.execute(message, id_auteur, date_pub, texte)
