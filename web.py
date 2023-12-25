"""

2021 - l'IUT de Valence - WOL - Ziyi Liu - Tuteur: Frédéric Michel; Christian Duccini

l'interface Web

"""


import cherrypy
import os,os.path
import logging
from mako.template import Template
from mako.lookup import TemplateLookup
from queue import Queue
from WolBD import BD_WOL
from WebFonction import *

#Si vous voulez modifier les Web page, les fichiers HTML sont dans le répertoire 'modeles'
mylookup=TemplateLookup(directories=['modeles'],module_directory='mako_modules')

logging.basicConfig(filename='web_log.log',level=logging.DEBUG)

        
class wol():
    """
    partie Web avec cherrypy
    """

    def __init__(self):
        """
        connecter au MySQL
        """
        self.bd=BD_WOL()
        self.pc=Fonction_WOL()
        self.raspi=Fonction_Raspi()

    @cherrypy.expose
    def index(self):
        """
        page Accueil
        """
        f=open('modeles/index.html',encoding="utf-8")
        s=f.read()
        return s

    @cherrypy.expose
    def Demarrer(self,hostname):
        """
        action de bouton 'Go' de la page Accueil
        récupérer l'adresse IP et l'adresse MAC depuis la BDD par hostname saisi (PC)
        ou récupérer le switch et le port depuis la BDD par hostname saisi (Raspi)
        puis demarrer la machine
        """
        if(hostname.startswith("Rasp")):
            position=self.bd.get_A_By_B("raspi","switch,port","hostname",hostname)
            self.raspi.poe(position[0],position[1],"auto")

            thread_demarrer=MyThread(mythread_raspi,args=(hostname,position[0]))
            thread_demarrer.start()
            thread_demarrer.join()
            
        else:
            allinfo=self.bd.get_A_By_B("pc","*","hostname",hostname)
            if(allinfo==()):  #si le hostname n'existe pas dans la BDD, retourne sur la page Accueil
                f=open('modeles/index.html',encoding="utf-8")
                s=f.read()
                return s
            ip=allinfo[2]
            mac=allinfo[3]
            if ip=="":
                f=open('modeles/no_ip.html',encoding="utf-8")
                s=f.read()
                return s

            thread_demarrer=MyThread(mythread_pc,args=(ip,mac))
            thread_demarrer.start()
            thread_demarrer.join()
    
        if thread_demarrer.get_resultat():  #si le port RDP (3389) de la machine est ouvert, return la page yes; sinon return la page no
            f=open('modeles/yes.html',encoding="utf-8")
            s=f.read()
            return s
        else:
            f=open('modeles/no.html',encoding="utf-8")
            s=f.read()
            return s

    def Table_Auth(self,salle,ordre):
        req="select addr_ip from pc where heure <> '';"
        list_ip=self.bd.execute(req)

        #détecter les PC activés, s'il n'est plus activé, met sa heure de démarrage en nulle
        q=Queue()
        for i in list_ip:  
            q.put(i[0])
        for x in range(len(list_ip)):
            t=MyThread(mythread_RDP,args=(q,))
            t.daemon=True
            t.start()
        q.join()

        resultat=self.bd.get_All("pc")
        pc_salle=[]
        for i in resultat:  #filtre salle, et obtenir les informations d'étudiants correspondance
            if(i[2].startswith(salle)):  #i[2] addr_ip
                ligne=list(i)
                info_etu=self.bd.get_A_By_B("etu","nom,gr","hostname",i[1])
                if(info_etu!=()):
                    ligne.extend([info_etu[0],info_etu[1]])
                else:
                    ligne.extend(["",""])
                pc_salle.append(ligne)

        d1=time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        t1=time.mktime(time.strptime(d1,"%a %b %d %H:%M:%S %Y"))
        r=[]
        for i in pc_salle:
            a=list(i)
            d2=a[4]  #récupérer heure de démarrage
            if d2!="": #calculer le temps depuis le démarrage
                t2=time.mktime(time.strptime(d2,"%a %b %d %H:%M:%S %Y"))
                t=t1-t2
                j=t//86400
                h=(t-j*86400)//3600
                m=(t-j*86400-h*3600)//60
                s=t-j*86400-h*3600-m*60
            else:
                j=h=m=s=0
            temps="{} jour(s) {}H {}M {}S".format(j,h,m,s)
            a.append(temps)
            r.append(a)  #[id,hostname,ip,mac,heure,nom,group,temps]
        r.sort(key=lambda s:s[int(ordre)]) #fonction de tri, ordre est la position de la valeur que vous souhaitez trier
        return r

    @cherrypy.expose
    def AuthR(self,login,password):
        """
        action de bouton 'Go' de la page Authentification
        page Authentification, si login et password sont correts, passe à la page supervision, sinon retourne sur la page Authentification
        """
        if(login=="root" and password=="root"):  #vous pouvez changer le valeur du login et password
            r=self.Table_Auth("","0") #toute les salle et ordre par id
            mytemplate=mylookup.get_template("supervision.html")
            return mytemplate.render(variable=r)
        else:
            f=open('modeles/Auth.html',encoding="utf-8")
            s=f.read()
            return s

    @cherrypy.expose
    def Renouveler(self,salle,ordre,textRe):
        """
        action de bouton 'Renouveler' de la page supervision
        refaire les ping, update heure de démarrer(si le PC ne répone pas) et temps de démarrer
        permettre de filtrer le tableau par salle (str "172.xx" ,defaut valeur "1")
        """
        r=self.Table_Auth(salle,ordre)
        s=r.copy()
        suprime=0
        if(textRe!=""): #filtrage par text de recherche, text surligné
            for a in range(0,len(r)):
                existe=False
                for b in range(1,len(r[a])):
                    if textRe.upper() in str(r[a][b]):
                        existe=True
                        s[a-suprime][b]=str(r[a][b]).replace(textRe.upper(),'<span style="background:yellow;">' + textRe + '</span>')
                if(not existe):
                    s.pop(a-suprime) #enlever la ligne qui ne contiens pas de textRe
                    suprime=suprime+1 #position va changer
        mytemplate=mylookup.get_template("supervision.html")
        return mytemplate.render(variable=s)

    @cherrypy.expose
    def Reveiller(self,hostname):
        """
        action de bouton 'Réveiller' de la page supervision
        envoyer un macig packet au PC
        refaire la page supervision comme AuthR
        """
        allinfo=self.bd.get_A_By_B("pc","*","hostname",hostname)
        ip=allinfo[2]
        mac=allinfo[3]

        self.pc.envoyer_wol(ip,mac)

        r=self.Table_Auth("","0")
        mytemplate=mylookup.get_template("supervision.html")
        return mytemplate.render(variable=r)

    @cherrypy.expose
    def Supprimer(self,pc):
        self.bd.delete_PC_By_Id(pc)
        
        r=self.Table_Auth("","0")
        mytemplate=mylookup.get_template("supervision.html")
        return mytemplate.render(variable=r)

    def Table_Raspi(self,switch):
        image_list=self.raspi.raspi_image_list()
        allinfo=self.bd.get_All("raspi")
        r=[]

        q_raspi=Queue()
        dict_image={}
        dict_recharge={}
        for i in allinfo:
            q_raspi.put(i[1])
        for x in range(len(allinfo)):
            t_raspi=MyThread(mythread_raspi_image,args=(q_raspi,dict_image,dict_recharge))
            t_raspi.daemon=True
            t_raspi.start()
        q_raspi.join()

        poe1=self.raspi.poe_status("@IP switch1")
        poe2=self.raspi.poe_status("@IP switch2")
        puissance1=self.raspi.raspi_status("@IP switch1")
        puissance2=self.raspi.raspi_status("@IP switch2")
        for i in allinfo:
            if(i[2].startswith(switch)): #filtrage switch
                allinfo_list=list(i)
                if(i[2]=="172.25.206.99"): #raspi du switch1
                    for x in poe1:
                        if(x[0]==i[3]): #port correspondance
                            poe_mode=x[1]
                            break
                    for y in puissance1:
                        if(y[0]==i[3]): #port correspondance
                            if(eval(y[3])>2): #Volt > 2, active
                                raspi_mode='<span style="color:green;">ON</span>'
                            else:
                                raspi_mode='<span style="color:red;">OFF</span>'
                            break
                else: #raspi du switch2
                    for x in poe2:
                        if(x[0]==i[3]):
                            poe_mode=x[1]
                            break
                    for y in puissance2:
                        if(y[0]==i[3]):
                            if(eval(y[3])>2):
                                raspi_mode='<span style="color:green;">ON</span>'
                            else:
                                raspi_mode='<span style="color:red;">OFF</span>'
                            break
                img=dict_image[i[1]]
                recharge=dict_recharge[i[1]]
                allinfo_list.extend([img,recharge,raspi_mode,poe_mode])
                r.append(allinfo_list) #[id,hostname,switch,port,image,recharge,status,poe_mode]
        return r,image_list

    @cherrypy.expose
    def Raspi(self):
        r,image_list=self.Table_Raspi("172.25")
        mytemplate=mylookup.get_template("raspi.html")
        return mytemplate.render(variable=r,image_list=image_list)

    @cherrypy.expose
    def Renouveler_Raspi(self,switch):
        r,image_list=self.Table_Raspi(switch)
        mytemplate=mylookup.get_template("raspi.html")
        return mytemplate.render(variable=r,image_list=image_list)

    @cherrypy.expose
    def Reveiller_Raspi(self,hostname):
        position=self.bd.get_A_By_B("raspi","switch,port","hostname",hostname)
        self.raspi.poe(position[0],position[1],"auto")
        r,image_list=self.Table_Raspi("172.25")
        mytemplate=mylookup.get_template("raspi.html")
        return mytemplate.render(variable=r,image_list=image_list)

    @cherrypy.expose
    def Arreter_Raspi(self,hostname):
        position=self.bd.get_A_By_B("raspi","switch,port","hostname",hostname)
        thread_arreter=MyThread(mythread_raspi_arret,args=("172.25.206."+hostname.replace("Rasp",""),position[0],position[1]))
        thread_arreter.start()
        r,image_list=self.Table_Raspi("172.25")
        mytemplate=mylookup.get_template("raspi.html")
        return mytemplate.render(variable=r,image_list=image_list)

    @cherrypy.expose
    def Stop_Raspi(self,hostname):
        position=self.bd.get_A_By_B("raspi","switch,port","hostname",hostname)
        self.raspi.poe(position[0],position[1],"shutdown")
        r,image_list=self.Table_Raspi("172.25")
        mytemplate=mylookup.get_template("raspi.html")
        return mytemplate.render(variable=r,image_list=image_list)

    @cherrypy.expose
    def Action_Raspi(self,choix,image,hostnames):
        if(choix==""):
            pass
        elif(choix=="reveiller"):
            if(type(hostnames)==str): #unique
                position=self.bd.get_A_By_B("raspi","switch,port","hostname",hostnames)
                self.raspi.poe(position[0],position[1],"auto")
            else:
                for i in hostnames: #multi
                    position=self.bd.get_A_By_B("raspi","switch,port","hostname",i)
                    self.raspi.poe(position[0],position[1],"auto")
        elif(choix=="arreter"):
            if(type(hostnames)==str):
                position=self.bd.get_A_By_B("raspi","switch,port","hostname",hostnames)
                thread_arreter=MyThread(mythread_raspi_arret,args=("172.25.206."+hostnames.replace("Rasp",""),position[0],position[1]))
                thread_arreter.start()
            else:
                for i in hostnames:
                    position=self.bd.get_A_By_B("raspi","switch,port","hostname",i)
                    thread_arreter=MyThread(mythread_raspi_arret,args=("172.25.206."+i.replace("Rasp",""),position[0],position[1]))
                    thread_arreter.start()
        elif(choix=="stop"):
            if(type(hostnames)==str):
                position=self.bd.get_A_By_B("raspi","switch,port","hostname",hostnames)
                self.raspi.poe(position[0],position[1],"shutdown")
            else:
                for i in hostnames:
                    position=self.bd.get_A_By_B("raspi","switch,port","hostname",i)
                    self.raspi.poe(position[0],position[1],"shutdown")
        elif(choix=="changer"):
            if(image!="" and type(hostnames)==str):
                actions=[hostnames.lower(),image]
                thread_script=MyThread(mythread_raspi_script,args=("changer_img.sh",actions))
                thread_script.start()
            elif(image!=""):
                for i in hostnames:
                    actions=[i.lower(),image]
                    thread_script=MyThread(mythread_raspi_script,args=("changer_img.sh",actions))
                    thread_script.start()
            else:
                pass
        elif(choix=="recharger"):
            if(type(hostnames)==str):
                actions=["4","2",hostnames.lower(),"y"]
                thread_script=MyThread(mythread_raspi_script,args=("menu_gestion.sh",actions))
                thread_script.start()
            else:
                for i in hostnames:
                    actions=["4","2",i.lower(),"y"]
                    thread_script=MyThread(mythread_raspi_script,args=("menu_gestion.sh",actions))
                    thread_script.start()
        else:
            pass

        r,image_list=self.Table_Raspi("172.25")
        mytemplate=mylookup.get_template("raspi.html")
        return mytemplate.render(variable=r,image_list=image_list)

if __name__=='__main__':
    rootPath=os.path.abspath(os.getcwd())
    print(rootPath)
    conf={
        '/':{'tools.sessions.on':True,
             'tools.staticdir.root':rootPath
            },
        '/static':{'tools.staticdir.on':True,
                   'tools.staticdir.dir':'modeles'
            },
        '/css':{'tools.staticdir.on':True,
                'tools.staticdir.dir':'modeles/css'  #chemain du css si vous avez besoin
            },
        '/images':{'tools.staticdir.on':True,
                   'tools.staticdir.dir':'modeles/images'
            }
        }
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})  #0.0.0.0 -> vous pouvez connecter par tous les interfaces du serveur
    cherrypy.quickstart(wol(),'/',conf)
