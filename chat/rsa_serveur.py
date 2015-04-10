#Programme de chat en ligne crypté en rsa

#**** devnotes *****

#08/04/2015: tout fonctionne normalement, il faut s'occuper de la communication mais la base est là.
#            Le client peut également être améliroé...



import threading
import socket
import sys
import time
import gadfly

#classe qui lit une base de donnée les id et mp des users
class base_de_donnée():
    def __init__(self):
        try:
            self.bdd = gadfly.gadfly("users", "D:/User/Documents/Programmes/Python Projects/RSA/files/")

#Classe de serveur (chaque serveur à un port attribué)
class serveur(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.arret_demande = False
        self.port = self.askPort()

        #si l'utilisateur a commandé l'arret du serveur:
        if self.arret_demande:
            return

        #sinon on continue
        self.nom = "Serveur-{}".format(self.port)


        #on rajoute le serveur dans le tableau :
        liste_serveur[self.port] = {"nom":self.nom, "clients":{}}

        #on lance le serveur
        self.start()

    #lance le serveur
    def run(self):

        #on lance la connexion du serveur
        try:
            self.socket_serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.socket_serveur.bind(("",self.port))
            self.socket_serveur.listen(5)
            print("-> Info : {} lancé sur le port({})".format(self.nom, self.port))
        except socket.error:
            print("-> Erreur : impossible de lancer {}.".format(self.nom))
            self.fermer_serveur()
            return

        #on attent une connexion
        while 1:
            #try:
             connexion, adresse = self.socket_serveur.accept()
             client(self.port, connexion, adresse)

            #except:
             #   print("-> Erreur : connexion erronée sur {}.".format(self.nom))
             #   self.fermer_serveur()
             #   return

    #demande le port du serveur à l'utilisateur
    def askPort(self):
        port = 0
        while 1: #tant que l'utilisateur ne rentre pas un port correcte :
            valide = True
            try:
                port = input("-> Port du serveur : ")
                for port_utilises in liste_serveur.keys():
                    if "{}".format(port_utilises) == port:
                        valide = False
                        print("-> {} est déja lancé sur ce port.".format(liste_serveur[port_utilises]["nom"]))

                if valide:
                    if port == "":
                        port = 40000
                        break
                    if port == "exit" or port == "cancel":
                        self.fermer_serveur()
                        return
                    port = int(port)
                    if port <= 65535 and port >= 0:
                        break

            except ValueError:
                print("-> Erreur : numero de port invalide.")
        return port

    #fermeture du serveur
    def fermer_serveur(self):
        try:
            del liste_serveur[self.port]
            self.socket_serveur.close()
            print("-> Info : {} a été interrompue.".format(self.nom))
        except (KeyError, AttributeError, TypeError):
            pass
        self.arret_demande = True

#classe de client lancée par un serveur lorsque qu'une connexion est demandée
class client(threading.Thread):

    def __init__(self, port, connexion, adresse):
        threading.Thread.__init__(self)

        #variables
        self.serveur_mère = liste_serveur[port]
        self.connexion = connexion
        self.adresse = adresse
        self.nom = self.getName().replace("Thread", "Client")


        #on ajoute le client au tableau général :
        self.serveur_mère["clients"][self.nom] = {"adresse":self.adresse, "connexion":self.connexion, "id":"n/a"}


        #lancement de la communication avec le client
        self.start()

    #la connexion est établie, on peut communiquer avec le client.
    def run(self):

        #on suit le schéma suivant:
        try:
            if self.identification_utilisateur(): #fonction qui demande à l'utilisateur id et mp
                self.communication() # si c'est ok, on peut communiquer

        #si il y a une erreur, on ferme la connexion:
        except:
            pass

        self.fermer_client()
        return

    def fermer_client(self):
        #on retire le client au tableau général :
        del self.serveur_mère["clients"][self.nom]

    #fonction qui demande à l'utilisateur id et mp
    def identification_utilisateur(self):

        while 1:
            self.connexion.send(b"ask.Login: ")
            login = self.connexion.recv(1024).decode()
            if login != "":
                #chercher dans base si login existe.
            self.connexion.send(b"txt.Login incorrect !")

    #communication serveur/client
    def communication(self):


#fonction qui gère le menu principal
def menu():
    #on laisse le temps d'executer les commandes
    time.sleep(0.5)

    choix = input("admin@localhost: ")

    if choix == "add":
        print("-> Ajout d'un serveur")
        new_serveur = serveur()

    elif choix == "quit":
        print("Merci d'avoir utilisé mon programme !")
        sys.exit()

    elif choix == "del":
        print("Suppression d'un serveur")

    elif choix == "help":
        print("add ; del ; check ; quit ; help")

    elif choix == "check":
        print(" Liste les serveurs : ")
        for serveur_de_liste in liste_serveur.values() :
            print("  *{}".format(serveur_de_liste["nom"]))
            for client in serveur_de_liste["clients"].values():
                print("    {}@{}".format(client["id"], client["adresse"][0]))


    else:
        print("Commande invalide")


liste_serveur = {}

while 1:
    menu()
