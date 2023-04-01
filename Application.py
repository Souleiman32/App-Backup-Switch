import tkinter as tk
import tkinter.ttk as ttk
import time
import datetime
from datetime import timedelta
import json
from crypto import encrypt_password,get_key

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Créer une fenetre 
root = tk.Tk()
root.title("Formulaire de saisie")
root.geometry("300x300")


#Fonction qui permet de créer un bar de progression
def my_function():
    progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    progress.place(relx=0.5, rely=0.6, anchor="center")
    progress.start()
    # Insérez ici le code de votre script
    
    
    for i in range(100):
        progress["value"] = i
        progress.update()
        time.sleep(0.1)
    from Backup import thread
    progress.destroy()

#Fonction qui permet de modifier le Path et nombre de jour de Purge
def Info_PP():
    data = json.load(open('Info.json'))
    
    Purge = Purge_entry.get()
    Path = Path_entry.get()

    if Path != "":
        data["Path"] = Path

    if Purge !="":    
        data["Purge"] = Purge


    Purge_entry.delete(0, 'end')
    Path_entry.delete(0, 'end')

    # Écriture du fichier json mis à jour
    with open("Info.json", "w") as json_file:
        json.dump(data, json_file)




#Fonction pour créer une nouvelle fenetre avec le formulaire
def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.geometry("300x280")
    new_window.title("Formulaire de saisie")

    # Créer les labels et les champs du formulaire

    hostname_label = tk.Label(new_window, text="Hostname:")
    hostname_label.pack()
    hostname_entry = tk.Entry(new_window)
    hostname_entry.pack()

    ip_label = tk.Label(new_window, text="Adresse Ip:")
    ip_label.pack()
    ip_entry = tk.Entry(new_window)
    ip_entry.pack()

    user_label = tk.Label(new_window, text="User:")
    user_label.pack()
    user_entry = tk.Entry(new_window)
    user_entry.pack()

    password_label = tk.Label(new_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(new_window)
    password_entry.pack()


    #Fonction pour revenir à la fenetre 1
    def go_back():
        new_window.destroy()
        root.deiconify()
        
    # Pour enregistrer les données saisies dans le fichier json
    def on_submit():
        hostname = hostname_entry.get()
        ip = ip_entry.get()
        password = password_entry.get()
        user = user_entry.get()

        key = get_key("key.key")
        data = json.load(open('database.json'))

        data.append({
                "hostname": hostname,
                "user":user,
                "adresse_ip": ip,
                "Password":f'{encrypt_password(password,key)}'
            })
        
        with open('database.json', 'w') as f:
            json.dump(data, f)

        hostname_entry.delete(0, 'end')
        ip_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        user_entry.delete(0, 'end')

    def showdata():
        def load_json(filepath):
            with open(filepath, "r") as file:
                data = json.load(file)
            return data

        def delete_line(listbox, data):
            selected_index = listbox.curselection()[0]
            del data[selected_index-1]
            listbox.delete(selected_index)
            save_json(data)

        def save_json(data):
            with open("database.json", "w") as file:
                json.dump(data, file)

        data = load_json("database.json")

        Show_data = tk.Toplevel(new_window)
        Show_data.title("Base de données")
        Show_data.geometry("300x280")

        listbox = tk.Listbox(Show_data,width=150)
        listbox.grid(row=0, column=0)
        listbox.pack()

        # Ajouter les colonnes "Hostname" et "Adresse IP" à la Listbox
        listbox.insert("end", "Hostname"  + " " * 45 + "Adresse ip")

        
        for item in data:
            listbox.insert("end",f"{item['hostname']}"  + " " * 40  + f"{item['adresse_ip']}")

        delete_button = tk.Button(Show_data, text="Supprimer", command=lambda: delete_line(listbox, data))
        delete_button.pack()


    

    #Bouton qui permet de retourner à la fenetre 1
    back_button = tk.Button(new_window, text="Retour", command=go_back)
    back_button.place(x=10, y=10)

    Save = tk.Button(new_window, text="Ajouter dans la BD",command=on_submit)
    Save.place(relx=0.5, rely=0.7, anchor="center")

    Show_data = tk.Button(new_window, text="Afficher la base de données",command=showdata)
    Show_data.place(relx=0.5, rely=0.85, anchor="center")

    


    new_window.mainloop()
    root.withdraw()



#Fonction pour Afficher l'historique du backup 

def history():

    # Lire le fichier JSON
    with open('Historique.json', 'r') as f:
        data = json.load(f)

    
     # Récupérer la date d'aujourd'hui
    now = datetime.datetime.now().date()
    # Calculez la date 7 jours auparavant
    seven_days_ago = now - timedelta(days=7)
    
    # Filtrer les entrées de données pour les 7 derniers jours
    filtered_data = [item for item in data if datetime.datetime.strptime(item['Date'], '%Y-%m-%d').date() >= seven_days_ago]

    # Récupérer les données nécessaires pour les graphiques
    dates = [item['Date'] for item in filtered_data]
    nombre_equipements = [int(item["Nombre d'équipements"]) for item in filtered_data]
    nombre_sauvegardes = [int(item["Nombre Equipements sauvegardés"]) for item in filtered_data]
    nombre_no_sauvegardes = [a-b for a, b in zip(nombre_equipements, nombre_sauvegardes)]



    # Initialiser la fenêtre Tkinter
    history = tk.Tk()
    history.title("Graphiques des données")

    try:
        fig1, ax1 = plt.subplots()
        # Plot Histogram
        bar1 = ax1.bar(dates, nombre_sauvegardes, color='blue', label='Nombre Equipements sauvegardés')
        bar2 = ax1.bar(dates,nombre_no_sauvegardes, color='red', label='Nombre d\'\u00e9quipements non sauvegardés')
        ax1.legend()
        ax1.set_xlabel('Dates')
        ax1.set_xticklabels(dates, rotation=90)
        ax1.set_ylabel('Nombre')
        ax1.set_title('Histogramme des équipements sauvegardés et non sauvegardés')

    
        # Ajouter les data labels sur les barres de l'histogramme
        for bar in bar1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2.0, height,
                    height, ha='center', va='bottom')
        for bar in bar2:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2.0, height,
                    height, ha='center', va='bottom')
  
        # Ajouter le histogramme à la fenêtre Tkinter
        canvas1 = FigureCanvasTkAgg(fig1, master=history)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Créer le diagramme en camembert
        fig2, ax2 = plt.subplots()
        labels = ['Sauvegardés', 'Non sauvegardés']
        sizes = [sum(nombre_sauvegardes), sum(nombre_equipements) - sum(nombre_sauvegardes)]
        explode = (0, 0.1)
        ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax2.axis('equal')

        # Ajouter le diagramme en camembert à la fenêtre Tkinter
        canvas2 = FigureCanvasTkAgg(fig2, master=history)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    except:
        next
    


    # Afficher la fenêtre Tkinter
    history.mainloop()





button1 = tk.Button(root, text="Start Backup",command=my_function)
button1.place(relx=0.5, rely=0.6, anchor="center")

button2 = tk.Button(root, text="Ajouter un équipement",command=open_new_window)
button2.place(relx=0.5, rely=0.75, anchor="center")


button3 = tk.Button(root, text="Enregistrer",command=Info_PP)
button3.place(relx=0.5, rely=0.4, anchor="center")

button4 = tk.Button(root, text="Afficher l'historique du Backup",command=history)
button4.place(relx=0.5, rely=0.9, anchor="center")

Path_label = tk.Label(root, text="Path:")
Path_label.pack()
Path_entry = tk.Entry(root)
Path_entry.pack()

Purge_label = tk.Label(root, text="Purge(jours):")
Purge_label.pack()
Purge_entry = tk.Entry(root)
Purge_entry.pack()




root.mainloop()



