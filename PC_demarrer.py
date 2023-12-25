# -*- coding: utf-8 -*

"""

2021 - l'IUT de Valence - WOL - Ziyi Liu - Tuteur: Michel Frédéric; Christian Duccini

Script au démarrage
permet tous les PC du salle C113, D102, D103, D106 d'envoyer ses informations (hostname, adresse IP, adresse MAC, heure de démarrage) au Serveur

"""

import socket
import uuid
import os
import time

IP=""
while(IP==""):  #attendre le service réseau démarre
        hostname=socket.gethostname()
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:  #obtenir les adresse ip de tous les interfaces
                if(ip.startswith("172.")):  #filtre les ip
                        IP=ip
mac=uuid.uuid1()
mac=mac.hex
mac=mac[-12:].upper()  #obtenir et mettre en forme l'adresse MAC (str "XXXXXXXXXXXX")
heure=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
data=hostname+'#'+IP+'#'+mac+'#'+heure

serv=IP.split(".")
serv_IP=serv[0]+"."+serv[1]+".0.10"  #trouver l'adresse IP de Serveur
s=socket.socket()
s.connect((serv_IP,8888))
s.send(data.encode())
s.close()

