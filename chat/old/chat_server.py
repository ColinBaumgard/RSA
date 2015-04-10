#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading
import time

#verrou de threading
verrou = threading.RLock()

#menu principale (dégeulasse)
def menu():
    time.sleep(0.5)
    choix = input("admin@localhost: ")

    if choix == "add":
        serveur.append(ThreadServeur())
        serveur[-1].start()

    elif choix == "quit":
        i = 1
        for thread_serveur in serveur:
            serveur[i].fermer
            i = i + 1

        sys.exit()

    elif choix == "del":
        while 1:
            try:
                i = 1

                for thread_serveur in serveur:
                    print("Serveur-{} = {}".format(i, thread_serveur))

                    i = i + 1
                num = int(input("Numero de serveur : "))

                if num > 0 and num <= len(serveur):
                    break
                else:
                    print("La valeur doit être comprise entre {} et {}".format(1, len(serveur)))

            except ValueError:
                print("Commande invalide")

        serveur[num-1].fermer
        del serveur[num-1]

    elif choix == "help":
        print("You are fucked-up because there is no help in this world !")

    elif choix == "check":
        i = 1
        for thread_serveur in serveur:
            print("Serveur-{} = {}".format(i, thread_serveur))
            i = i + 1

    else:
        print("Commande invalide")

#fonction qui vérifie l'identifiant et le mpd de l'utilisateur (test) ; retourn l'id
def connecter_user(connexion, ip):
    while 1: #tant que l'on a pas rentré le bon id;mdp ou exit :
        connexion.send(b"ask.Login: ")
        user_id = connexion.recv(1024).decode()
        connexion.send(bytes("ask.{}@{}'s password: ".format(user_id, ip), "utf-8"))
        user_pw = connexion.recv(1024).decode()

        if user_id == "Colin":
            if user_pw == "coucou":
                return user_id
            else:
                connexion.send(b"Mauvais mot de passe.")
        elif user_id == "exit":
            return 0
        else:
            print("Mauvais login.")

#classe de thread de client attaché a un serveur ThreadServeur
class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    def __init__(self, serveur_mère):
        threading.Thread.__init__(self) #héritage
        self.serveur_mère = serveur_mère
        self.nom = self.getName().replace("Thread", "Client")
        self.connexion = self.serveur_mère.getConnexion()
        self.user_ip = ip
        self.user_id = ""

    def run(self):

        # Demande d'identification :
        try:
            self.user_id = connecter_user(self.connexion, self.user_ip)
            if self.user_id == 0:
                self.deconnexion_Client()

        except (ConnectionResetError, NameError): #si erreur, on supprime le thread du tab et on quitte
            tb_client[self.nom] = 0
            self.deconnexion_Client()



        # Dialogue avec Client :

        self.connexion.send('\n***********************\nServeur de chat en RSA (v0.1)(02/04/2015)(Colin Baumgard)\n***********************\n\n'.encode())

        while 1:
            try:
                self.connexion.send(bytes("ask.{}@{}:".format(self.user_id, self.user_ip), "utf-8"))
                msgClient = self.connexion.recv(1024)
                if msgClient.upper() == "FIN" or msgClient =="":
                    self.deconnexion_Client()
                else:
                    pass

            except (ConnectionResetError, NameError):
                tb_client[self.nom] = 0
                self.deconnexion_Client()

    def deconnexion_Client(self):
        # Fermeture de la connexion :
        self.connexion.close()
        del tb_client[self.nom]
        print ("Client %s déconnecté." % self.nom)
        return


#classe de thread de seveur qui lancent des threadServeurs
class ThreadServeur(threading.Thread):

    #consructeur qui définie l'objet Serveur. On demande le port.
    def __init__(self):
        threading.Thread.__init__(self)
        self.port = self.getPort()
        self.hote = ""
        self.socket_serveur = 0
        self.connexion = 0
        self.nom = self.getName().replace("Thread", "Serveur")

    #on peut lancer et arreter le serveur à ça guise.
    def run(self):

        #on lance la connexion du serveur
        try:
            self.socket_serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.socket_serveur.bind((self.hote,self.port))
            self.socket_serveur.listen(5)
            print("Info : {} lancé sur le port({})".format(self.nom, self.port))
        except socket.error:
            print("Erreur : impossible de lancer le serveur.")


        while 1:
            try:
                self.connexion, self.adresse = self.socket_serveur.accept()
            except:
                print("Vous avez déja un serveur lancé sur ce port... ")
                return
            th = ThreadClient(self.connexion, self.adresse[0])
            th.start()
            # Mémoriser la connexion dans le dictionnaire
            id_thread = th.getName().replace("Thread", "Client")
            tb_client[id_thread] = self.connexion
            print ("Client: %s connecté, adresse IP: %s, port: %s." % (id_thread, self.adresse[0], self.adresse[1]))

    #demande le port à l'utilisateur
    def getPort(self):
        port = 0
        while 1: #tant que l'utilisateur ne rentre pas un port correcte :
            try:
                port = input("Port du serveur : ")
                if port == "":
                    port = 40000
                    break
                if port == "exit" or port == "cancel":
                    self.fermer()
                    time.sleep(1)
                    break
                port = int(port)
                if port <= 65535 and port >= 0:
                    break

            except ValueError:
                print("Erreur : numero de port invalide.")
        return port

    #se charge de fermer le serveur proprement
    def fermer(self):
        self.connexion.send(b"Fermeture de la connexion")
        self.connexion.send(b"end")
        print("Info : Fermeture de la connexion")
        self.socket_serveur.close()
        print("Info : Connexion interrompue")




tb_client = [{}] #dicitonnaire{nom thread ; connexion)
serveur = []   #tableau de serveur

while 1:
    menu()

