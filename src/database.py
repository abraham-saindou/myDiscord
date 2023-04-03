import mysql.connector
from classes.message import *

db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "MyDiscord"
)

cursor = db.cursor(prepared=True)


#Recupere l'id d'un utilisateur a partir de son nom
def get_user_id(l_name, f_name):
    cursor.execute("SELECT id FROM utilisateurs WHERE nom = ? AND prenom = ?", [l_name, f_name])
    result = cursor.fetchone()

    return result[0]

#Recupere le nom d'un utilisateur a partir de son id
def get_username(id):
    cursor.execute("SELECT nom, prenom FROM utilisateurs WHERE id = ?", [id])
    result = cursor.fetchall()
    return " ".join(result[0])

def get_users():
    cursor.execute("SELECT nom, prenom FROM utilisateurs")
    result = cursor.fetchall()

    users = []
    for u in result:
        users += [" ".join(u)]
    
    return users

def get_channels():
    cursor.execute("SELECT * FROM canaux")
    result = cursor.fetchall()
    return result

#Recupere les messages publics
def get_channel_messages(channel):
    cursor.execute("SELECT * FROM messages WHERE id_canal = ?", [channel])
    result = cursor.fetchall()

    messages = []
    for m in result:
        messages += [Messages(m[1], m[2], f"({m[2]}) {get_username(m[1])}: {m[3]}", m[4])]

    return messages

#Recupere les messages privés entre user1 et user2
def get_private_messages(user1, user2):

    cursor.execute("SELECT * FROM messages \
                   WHERE (id_auteur = ? AND id_destinataire = ?) \
                   OR (id_auteur = ? AND id_destinataire = ?)", [user1, user2, user2, user1])
    
    result = cursor.fetchall()

    messages = []
    for m in result:
        
        messages += [Messages(m[1], m[2], f"({m[2]}) {get_username(m[1])}: {m[3]}", m[4], m[5])]

    return messages


channels = get_channels()
channels_dict = dict(channels)
channels_id_dict = {v: k for k, v in channels_dict.items()}