"""

2021 - l'IUT de Valence - WOL - Ziyi Liu - Tuteur: Michel Frédéric; Christian Duccini

Script serveur
Recevoir des informations du PC (hostname, adresse IP, adresse MAC) et renouveller la base de données

"""

import socket
import time
from WolBD import BD_WOL
import logging

logging.basicConfig(filename="Serveur_information_log",level=logging.DEBUG)

mesPCs=BD_WOL()

s=socket.socket()
s.bind(('0.0.0.0',8888))
s.listen(50)

while True:
    c,addr=s.accept()
    logging.info("Client : {}, adresse {} , connect".format(addr[0],addr[1]))
    data=c.recv(1024)
    data=data.decode()
    data=data.split('#')
    hostname=data[0]
    ip=data[1]
    mac=data[2]
    heure=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    logging.info("Hostname : {} ; addr_ip : {} ; addr_mac : {} ; heure : {}".format(hostname,ip,mac,heure))

    hostlist=mesPCs.get_A("pc","hostname")
    ancien_host=mesPCs.get_A_By_B("pc","hostname","addr_ip",ip)
    if ancien_host!=():
        mesPCs.set_Ip_Null(ip)
        logging.info("Remplace ancien IP du {}".format(ancien_host[0]))
    if hostname in hostlist:
        mesPCs.update_PC(hostname,ip,mac,heure)
        logging.info("Update addr_ip, addr_mac et heure du {}".format(hostname))
        logging.info("----------")
    else:
        mesPCs.insert_PC(hostname,ip,mac,heure)
        logging.info("Ajouter {} dans la base de donnée".format(hostname))
        logging.info("----------")
