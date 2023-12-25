"""

2021 - l'IUT de Valence - WOL - Ziyi Liu - Tuteur: Michel Frédéric; Christian Duccini

Fonctions de la base de données

1. créer une base de donnée s'appelle 'wol'
créer tables 'pc' (id, hostname, addr_ip, addr_mac, heure)
             'raspi' (id, hostname, switch, port)
             'etu' (nom, hostname,gr)
2. renouveller table 'etu' par fichier 'etudiants.csv'

"""

import pymysql
from os import getcwd

_host="localhost"
_user="root"
_pass="iutval"
_nomBase="wol"
    
# les 2 fonctions suivantes permettent de récupérer une connexion et un curseur
def getdb(host=_host,user=_user,passwd=_pass,dbname=_nomBase) :
    import pymysql
    dbo=pymysql.connect(host=host,user=user,passwd=passwd,db=dbname)
    c=dbo.cursor()
    return (dbo,c)
    
def createdb(host=_host,user=_user,passwd=_pass) :
    import pymysql
    dbo=pymysql.connect(host=host,user=user,passwd=passwd)
    c=dbo.cursor()
    return (dbo,c)

class BD_WOL(object) :
    """  un objet "BD_WOL" permettra d'interagir avec la table "pc" stockée dans une base MySQL supposée créée et
    dont la structure est définie ci-dessus) """
    def __init__(self):
        """ Constructeur de l'objet BD_pc (en fait connexion à la base existante """
        self._db, self._c=getdb()
            
    def execute(self,req) :
        self._db, self._c=getdb()
        res=self._c.execute(req)
        if "select" in req :
            res=self._c.fetchall()
        else :
            self._db.commit()
        return res

    def get_All(self,table):
        """ Rend tous dans la table
        """
        req="select * from {} order by id;".format(table)
        r=self.execute(req)
        return r

    def get_A_By_B(self,table,A,B,value_B):
        """ get_A_By_B() -> select "A" from "table" where "B"="value_B"
        Rend le contenu de la base sous forme d'une liste"""
        req="select {} from {} where {}='{}';".format(A,table,B,value_B)
        r=self.execute(req)
        if len(r)==0:
            return r
        elif len(r)==1:
            return r[0]
        else:
            x=[]
            for i in r:
                x.append(i[0])
            return x

    def get_A(self,table,A):
        """ get_A -> select "A" from "table
        Rend la liste des "A" dans la base """
        req="select {} from {};".format(A,table)
        r=[]
        for i in self.execute(req):
            r.append(i[0])
        return r

    def update_PC(self,hostname,ip,mac,heure):
        """update pc set addr_ip="ip", addr_mac="mac", heure="heure" where hostname="hostname"
        Mise à jour des infos d'un pc dans la table "pc" par hostname """
        req="update pc set addr_ip='{}',addr_mac='{}',heure='{}' where hostname='{}';".format(ip,mac,heure,hostname)
        self.execute(req)

    def update_PC_A_By_B(self,A,B,value_A,value_B):
        """update pc set "A"="value_A" where "B"="value_B"
        Mise à jour une valeur"""
        req="update pc set {}='{}' where {}='{}';".format(A,value_A,B,value_B)
        self.execute(req)

    def set_Ip_Null(self,ip):
        """update pc set addr_ip='' where addr_ip="ip"
        Mise à jour addr_ip à nulle par addr_ip"""
        req="update pc set addr_ip='' where addr_ip='{}';".format(ip)
        self.execute(req)

    def insert_PC(self, hostname, ip, mac, heure):
        """ Insertion d'un pc dans la base de données"""
        req="insert into pc values (NULL,'{}','{}','{}','{}');".format(hostname,ip,mac,heure)
        self.execute(req)

    def reload_Etu(self, filename="etudiants.csv"):
        """ Chargement des étudiants à partir d'un fichier etudiants.csv"""
        self.execute("delete from etu;")
        f=open('{}\{}'.format(getcwd(),filename),encoding='utf-8')
        for ligne in f:
            r = ligne.split(',')
            req="insert into etu values ('{}','{}','{}');".format(r[0]+r[1],r[3],r[2])
            self.execute(req)
            
    def reload_Raspi(self, filename="raspi.csv"):
        """ Chargement des Raspberry Pi à partir d'un fichier raspi.csv"""
        self.execute("delete from raspi;")
        f=open('{}\{}'.format(getcwd(),filename),encoding='utf-8')
        for ligne in f:
            r = ligne.split(',')
            req="insert into raspi values ('{}','{}','{}','{}');".format(r[0],r[1],r[2],r[3])
            self.execute(req)

    def delete_PC_By_Id(self, pc_id):
        """ Suppression d'un device par son Id"""
        req="delete from pc where id='{}';".format(pc_id)
        self.execute(req)
            
if __name__ == "__main__" :
    action=input("Action  1)créer base de données wol 2)update table etu 3)update table raspi : ")
    if(action=="1"):
        reqCreation1="create table pc ( id int primary key auto_increment, hostname varchar(32) not null, ip varchar(32) not null, mac varchar(32) not null, heure varchar(64) not null);"
        reqCreation2="create table raspi ( id int primary key auto_increment, hostname varchar(32) not null, ip varchar(32) not null, mac varchar(32) not null, heure varchar(64) not null);"
        reqCreation3="create table etu ( numero int primary key, nom varchar(32) not null, hostname varchar(32) references pc(hostname),gr varchar(16));"
        db,c = createdb(dbname="")
        c.execute("create database {}".format(_nomBase))
        c.execute("use {}".format(_nomBase))
        c.execute(reqCreation1)
        c.execute(reqCreation2)
        c.execute(reqCreation3)
        db.commit()
        print("Base créée : {}".format(db))
    elif(action=="2"):
        bd=BD_WOL()
        bd.reload_Etu()
        print("update table etu")
    elif(action=="3"):
        bd=BD_WOL()
        bd.reload_Raspi()
        print("update table raspi")
    else:
        print("Pas cet action")
