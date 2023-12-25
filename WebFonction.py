"""

2021 - l'IUT de Valence - WOL - Ziyi Liu - Tuteur: Michel Frédéric; Christian Duccini

Fonctions du Web
    envoyer packet magique
    connecter le port RDP

    connecter le serveur Raspi / le switch / le Raspberry Pi
    ping
    changer PoE mode du switch
    PoE Port status du swtich (PoE mode)
    PoE status du switch (puissance du port -> raspi status)
    liste d'image dans le répertoire /srv/images du serveur
    arrêter Raspi
    détecter image du Raspi
    lancer script bash de serveur Raspi

Thread
    réveiller PC
    détecter status du PC
    réveiller Raspi
    arrêter Raspi
    lancer script bash de serveur Raspi
    détecter image du Raspi

"""

import pymysql
import socket
import paramiko
import threading
import binascii
import time
import os
from WolBD import BD_WOL

class Fonction_WOL():

    def __init__(self):
        pass

    def envoyer_wol(self,ip,mac):
        data_envoyer='FF'*6+str(mac)*16 #contenu du packet magique
        data=binascii.unhexlify(data_envoyer) #transmettre hexadécimal à binaire
        port=9
        ip_valeur=ip.split(".")
        broadcast=ip_valeur[0]+"."+ip_valeur[1]+".255.255"
        s_wol=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #family:AF_INET(entre serveur) type:UDP (paquet, non connecté)
        s_wol.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) #diffusion LAN 
        s_wol.sendto(data,(broadcast,port))
        return True

    def RDP(self,ip):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #family:AF_INET type:TCP
        r=s.connect_ex((ip,3389))
        s.close()
        return r==0

class Fonction_Raspi():

    def __init__(self):
        self.switch1="172.25.206.99"
        self.switch2="172.25.206.98"
        self.serveur="172.25.206.100"

    def connexion_switch(self,switch):
        trans=paramiko.Transport((switch,22)) #instancier objet transport
        trans.connect(username="ubnt", password="iutval26")
        chan=trans.open_session() #ouvrir session
        chan.get_pty() #ouvrir terminal
        chan.invoke_shell()
        return trans,chan

    def connexion_serveur(self):
        trans=paramiko.Transport((self.serveur,22))
        trans.connect(username="iutuser", password="iutval")
        chan=trans.open_session()
        chan.get_pty()
        chan.invoke_shell()
        return trans,chan

    def connexion_raspi(self,ip):
        trans=paramiko.Transport((ip,22))
        trans.connect(username="pi", password="raspberry")
        chan=trans.open_session()
        chan.get_pty()
        chan.invoke_shell()
        return trans,chan

    def ping(self,ip):
        cmd= ["ping", "-n","1", ip]  #sous Windows utilise -n; sous Linux utilise -c
        output = os.popen(" ".join(cmd)).readlines() #obtenir le resultat de "ping"
        flag = False
        for line in list(output):
            if not line:
                continue
            if str(line).upper().find("TTL") >=0:
                flag = True
                break
        return flag

    def poe(self,switch,port,status):
        trans,chan=self.connexion_switch(switch)
        chan.send("en"+"\n")
        chan.send("iutval26"+"\n")
        chan.send("conf"+"\n")
        chan.send("interface {}".format(port)+"\n")
        chan.send("poe opmode {}".format(status)+"\n") #changer poe mode
        time.sleep(1)
        chan.close()
        trans.close()

    def poe_status(self,switch):
        trans,chan=self.connexion_switch(switch)
        chan.send("en"+"\n")
        chan.send("iutval26"+"\n")
        chan.send("show poe port all"+"\n")
        chan.send(" ")
        time.sleep(1)
        poe_switch=chan.recv(65535).decode() #obtenir le resultat du command "show poe port all"
        chan.close()
        trans.close()
        #nettoyer le resultat, sous forme list ((Intf,OP Mode,HP Enable, HP Mode, Detect Enable, Disconnect Enable, Class Enable),...)
        poe_switch=poe_switch.split("-------")
        poe_switch_info=poe_switch[-1]
        poe_switch_info=poe_switch_info.replace("--More-- or (q)uit\r                  \r","")
        poe_switch_info=poe_switch_info.replace("(UBNT EdgeSwitch) #","")
        poe_switch_infolist=poe_switch_info.split("\r\n")
        poe=[]
        for i in poe_switch_infolist:
            z=i.split(" ")
            while("" in z):
                z.remove("")
            if(z!=[]):
                poe.append(z)
        return poe

    def raspi_status(self,switch):
        trans,chan=self.connexion_switch(switch)
        chan.send("en"+"\n")
        chan.send("iutval26"+"\n")
        chan.send("show poe status all"+"\n")
        chan.send(" ")
        time.sleep(1)
        poe_switch=chan.recv(65535).decode()
        chan.close()
        trans.close()
        #nettoyer le resultat, sous forme list ((Intf, Detection, Class, Consumed(W), Voltage(V), Current(mA), Consumed Meter(Whr), Temperature(C),...)
        poe_switch=poe_switch.split("-------")
        poe_switch_info=poe_switch[-1]
        poe_switch_info=poe_switch_info.replace("--More-- or (q)uit\r                  \r","")
        poe_switch_info=poe_switch_info.replace("(UBNT EdgeSwitch) #","")
        poe_switch_infolist=poe_switch_info.split("\r\n")
        poe=[]
        for i in poe_switch_infolist:
            z=i.split("  ")
            while("" in z):
                z.remove("")
            if(z!=[]):
                poe.append(z)
        return poe

    def raspi_image_list(self):
        trans,chan=self.connexion_serveur()
        chan.send("ls /srv/images"+"\n")
        time.sleep(0.5)
        r=chan.recv(65535).decode()
        chan.close()
        trans.close()
        #nettoyer le resultat, sous forme list (image1,image2,...)
        image_list=r.split("ls /srv/images")[-1]
        image_list=image_list.replace("\r\n"," ").replace("iutuser@debian:~$"," ").replace("\x1b[0m"," ").replace("\x1b[01;32m"," ")
        image_list=image_list.split(" ")
        while("" in image_list):
            image_list.remove("")
        return image_list

    def raspi_arret(self,ip,switch,port):
        trans,chan=self.connexion_raspi(ip)
        chan.send("sudo shutdown -h now"+"\n")
        time.sleep(0.5)
        chan.close()
        trans.close()
        while(self.ping(ip)):
            time.sleep(5)
        time.sleep(5)
        self.poe(switch,port,"shutdown")

    def raspi_image(self,hostname):
        trans,chan=self.connexion_serveur()
        chan.send("ls /srv/nfs/{}/iso".format(hostname.lower())+"\n")
        time.sleep(0.5)
        r=chan.recv(65535).decode()
        #nettoyer le resultat, sous forme list (nom_image,)
        image=r.split("ls /srv/nfs/{}/iso".format(hostname.lower()))[-1]
        image=image.replace("\r\n","").replace("iutuser@debian:~$","").replace("\x1b[0m","").replace("\x1b[01;32m","")
        image=image.split(" ")
        while("" in image):
            image.remove("")
        if("image.img" in image):
            image.remove("image.img")
        else :
            image.insert(0,"no image")

        chan.send("ls /srv/tftp/{}".format(hostname.lower())+"\n")
        time.sleep(0.5)
        r=chan.recv(65535).decode()
        chan.close()
        trans.close()
        if("cmdline.txt" in r):
            recharge="Yes"
        else:
            recharge="No"
        if(image==[]): #si l'image est en train de copier (dans répertoire /srv/nfs/raspX/iso a seulement un fichier "image.img"
            image_v="copier..."
        else:
            image_v=image[0]
        return image_v,recharge
        
    def script(self,script,actions):
        trans,chan=self.connexion_serveur()
        chan.send("su"+"\n")
        time.sleep(1)
        chan.send("iutval"+"\n")
        time.sleep(1)
        chan.send("bash /srv/script/{}".format(script)+"\n")
        time.sleep(1)
        for i in actions:
            chan.send(i+"\n")
            time.sleep(1)

class MyThread(threading.Thread):

    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func=func
        self.args=args

    def run(self):
        self.r=self.func(*self.args)

    def get_resultat(self):
        threading.Thread.join(self)
        return self.r

def mythread_pc(ip,mac):
    mesPCs=Fonction_WOL()
    i=0
    access=False
    while(i<55 and not access):  #ressayer envoyer Magic Packet dans environ 3 minutes jusqu'à la machine réponse
        mesPCs.envoyer_wol(ip,mac)
        access=mesPCs.RDP(ip)
        time.sleep(5)
        i=i+5
    return access

def mythread_RDP(q):
    ip=q.get() #obtenir ip depuis la queue q
    bd=BD_WOL()
    mesPCs=Fonction_WOL()
    if(mesPCs.RDP(ip)):
        pass
    else:
        bd.updata_PC_A_By_B("heure","","addr_ip",ip) #ne peut pas accéder au PC, mettre heure de demarrage à nulle
    q.task_done()
            
def mythread_raspi(hostname,switch):
    ip="172.25.206."+hostname.replace("Rasp","") #obtenir l'adresse IP (172.25.206.X) du RaspX
    mesRaspi=Fonction_Raspi()
    i=0
    access=False
    while(i<55 and not access): 
        access=mesRaspi.ping(ip)
        time.sleep(5)
        i=i+5
    return access

def mythread_raspi_arret(ip,switch,port):
    mesRaspi=Fonction_Raspi()
    mesRaspi.raspi_arret(ip,switch,port)

def mythread_raspi_script(script,actions):
    mesRaspi=Fonction_Raspi()
    mesRaspi.script(script,actions)

def mythread_raspi_image(q,dict_image,dict_recharge):
    hostname=q.get()
    mesRaspi=Fonction_Raspi()
    image,recharge=mesRaspi.raspi_image(hostname)
    dict_image[hostname]=image #mettre le valeur dans le dictionnaire
    dict_recharge[hostname]=recharge
    q.task_done()
