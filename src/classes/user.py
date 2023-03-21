import mysql.connector

class User:
    def __init__(self, name, fname, email, pwd):
        self.lastname = name
        self.firstname = fname
        self.email = email
        self.password = pwd
        self.connected = False

    def register(self, db):
        db.execute("SELECT * FROM Utilisateurs WHERE email = ?", [self.email])
        
        search = db.fetchall()

        if not search:
            db.execute("INSERT INTO Utilisateurs (nom, prenom, email, motdepasse) VALUES\
                       (?,?,?,?)", [self.lastname, self.firstname, self.email, self.password])
        
        else:
            print("Cette addresse est deja utilisée")

        pass
    
    def connection(self, db):

        db.execute("SELECT motdepasse FROM Utilisateurs WHERE email = ?", [self.email])
        search = db.fetchall()
        if self.password == search:
            self.connected = True
        

    def deconnection(self, db):
        self.connected = False