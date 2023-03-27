from database import *

class User:
    def __init__(self, email, pwd, name="", fname=""):
        self.lastname = name
        self.firstname = fname
        self.email = email
        self.password = pwd

    #Ajoute un utilisateur dans la bdd si il n'est pas deja present
    def register(self):
        cursor.execute("SELECT * FROM Utilisateurs WHERE email = ?", [self.email])
        
        search = cursor.fetchall()

        if not search:
            cursor.execute("INSERT INTO Utilisateurs (nom, prenom, email, motdepasse) VALUES\
                       (?,?,?,?)", [self.lastname, self.firstname, self.email, self.password])
            db.commit()
            print("added succesfully")
            return True
        
        return False
    
    #Connecte l'utilisateur si le mot de passe entré correspond a celui dans la bdd
    def connection(self):

        cursor.execute("SELECT * FROM Utilisateurs WHERE email = ?", [self.email])
        search = cursor.fetchall()

        if not search:
            return False
        
        if self.password == search[0][4]:

            self.id = search[0][0]
            self.lastname = search[0][1]
            self.firstname = search[0][2]

            return True
        return False
        