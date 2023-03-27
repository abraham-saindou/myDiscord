import mysql.connector
from classes.message import *

db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "SuperP3scado",
        database = "MyDiscord"
)

cursor = db.cursor(prepared=True)



#Recupere l'id d'un utilisateur a partir de son nom
def get_user_id(l_name, f_name):
    cursor.execute("SELECT id FROM Utilisateurs WHERE nom = ? AND prenom = ?", [l_name, f_name])
    result = cursor.fetchone()
    return result[0]

#Recupere les messages publics
def get_public_messages():
    cursor.execute("SELECT * FROM Messages WHERE id_canal = 0")
    result = cursor.fetchall()

    messages = []
    for m in result:
        messages += [Message(m[1], m[2], m[3], m[4])]

    return messages

#Recupere les messages privés entre user1 et user2
def get_private_messages(user1, user2):

    cursor.execute("SELECT * FROM Message \
                   WHERE id_canal = 1 \
                   AND (id_auteur = ? AND id_destinataire = ?) \
                   OR (id_auteur = ? AND id_destinataire = ?)", [user1, user2, user2, user1])
    
    result = cursor.fetchall()
    
    messages = []
    for m in result:
        messages += [Message(m[1], m[2], m[3], m[4], m[5])]

    return messages
    