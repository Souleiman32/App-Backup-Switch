import  netmiko
import threading
import os
from datetime import datetime
import json
from crypto import decrypt_password,get_key
from Purge import purge
import time
now = datetime.now()

year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute



#Récuperer les informations du fichier json Info
with open('Info.json') as f:
    Info = json.load(f)
    Path = Info["Path"]
    day_purge = Info["Purge"]


#Récuperer les informations du fichier json database
with open("database.json") as json_data:
    data_dict = json.load(json_data)


def Backup(Path,hostname,username,adresse_ip,password):


    device = {
    'device_type': 'cisco_ios', #check_point_gaia
    'ip': adresse_ip,
    'username': username,
    'password': password, 

    }



    #Connecter à l'équipement
    net_connect = netmiko.ConnectHandler(**device)

    # Envoyer la commande show the running configuration
    output = net_connect.send_command("show run")#show configuration


    Path_F = fr'{Path}\\Equipements\\{hostname.replace(" ", "_")}'
    # Vérifier si le dossier existe , si non le crée
    if not os.path.exists(Path_F):
        os.makedirs(Path_F)
    # Crée un fichier texte : sous la forme de hostname-date-adresse_ip
    myFile = open(
        f'{Path_F}' + f"\\{hostname.replace(' ', '_')}" + "-{}-{}-{}_{}.txt".format(day,
                                                                                    month,
                                                                                    year,
                                                                                    adresse_ip),
        "w+")
    # Ecrire dans le fichier la sortie de l'output

    output = output.replace("Building configuration...", "")
    lines = output.splitlines()

    for line in lines[2:]:
        if line:
            myFile.write(line + '\n')

    #myFile.write(output)
    myFile.close()

    # Fermer la conexion
    net_connect.disconnect()
    purge(day_purge,Path_F)







# -----------------------------------------------------------------------------------------------------------------------------------------------------------#
"""
Cette fonction permet de récupérer la date du fichier en second 
"""


def get_file_or_folder_age(path):
    t = os.stat(path).st_ctime
    return t


# ------------------------------------------------------------------------------------------------------------------------------------------------------------#
"""
Cette fonction permet d'ajouter les équipements sauvegardés et les équipements non sauvegarder dans leurs listes ,vérifier si c'est des sauvegardes du jour 
"""
def stat_device(path, ip):
    l1 = []
    # récupérer la date du jour en second
    d = time.time()
    # Virifier si le dossier Path existe
    if os.path.exists(path):
        # Parcourir les sous-repertoire et les fichiers dans ce dossier Path
        for root, dirs, files in os.walk(path):
            for name in files:
                try:
                    t = os.path.join(path, name)
                    # calculer la difference en second entre la date de jour et la date de créaction du fichier
                    df = d - get_file_or_folder_age(t)
                    # Vérifier si le fichier de sauvegarde finit par ip.txt ...
                    if name.endswith(f"{ip}.txt") and df < 3600*24:
                        l1.append(ip)
                    else:
                        pass
                except:   
                    next
    else:
        pass

    return l1

#Cette fonction permet d'écrire l'historique dans le fichier json
def SetData(date,eq,eq_ok,list_eq):


    data = json.load(open('Historique.json'))

    data.append({
        "Date": date,
        "Nombre d'\u00e9quipements": eq,
        "Nombre Equipements sauvegardés":eq_ok,
        "Noms d'\u00e9quipements non sauvegardés": list_eq
        })
    
    with open('Historique.json', 'w') as f:
        json.dump(data, f)


#Cette fonction permet d'avoir la liste des équipements et les équipements non sauvegardés 

def Data():
    l1 = []
    l2 = []
    for data in data_dict:
        hostname = data['hostname']
        ip = data['adresse_ip']
        l1.append(ip)
        Path_F = fr'{Path}\\Equipements\\{hostname.replace(" ", "_")}'
        l2.extend(stat_device(Path_F, ip))
        

    return set(l1), set(l2)




def thread():

# Liste vide pour stocker les threads
    threads = list()
    for data in data_dict:
        hostname = data["hostname"]
        username = data['user']
        adresse_ip = data['adresse_ip']
        password = data['Password']
       
        try:
            t = threading.Thread(target=Backup, args=(Path,hostname,username,adresse_ip,decrypt_password(password.encode(),get_key("key.key"))))
            threads.append(t)
        except:
            next

    for t in threads:
        t.start()
        t.join()

    #Pour envoyer l'historique du Backup : Date , nombre d'équipement , nombre d'équipement sauvegardés , liste des adresse Ip non sauvegardés
    SetData(f"{datetime.now().date()}",len(set(Data()[0])),len(set(Data()[1])),list(set(Data()[0]) ^ set(Data()[1])))


thread()




 
