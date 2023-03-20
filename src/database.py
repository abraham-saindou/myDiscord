import mysql.connector


class SQL:
    def __init__(self, hote, utilisateur, mdp, database):
        self.connector = mysql.connector.connect()
        self.cursor = self.connector.cursor()

    def new_user(self, nom, prenom, mail, mdp):
        insert = "INSERT INTO utilsateurs(nom, prenom, email, mdp)"
        self.cursor.execute(insert)

    def add_message(self):
        message = "INSERT INTO messages(id_auteur, date_pub, texte)"
        self.cursor.execute(message)
