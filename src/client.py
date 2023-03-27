from tkinter import *
from database import *
from classes.gui import *

app = Interface()
app.run()

#clos la connexion si le client est toujours connecté a la fermeture du programme
try:
    message = "{quit}"
    app.client.sendall(message.encode())
    app.client.close()
except:
    pass

cursor.close()