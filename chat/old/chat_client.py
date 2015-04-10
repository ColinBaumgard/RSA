import socket

class serveur():

    def __init__(self):
        self.port = 0
        self.hote = "localhost"
        self.identifiant = ""
        self.mot_de_passe = ""

    #assure une premiere connection avec le serveur ( demande port & adresse )
    def connecter(self):
        while 1:
            while 1: #tant que l'utilisateur ne rentre pas un port correcte :
                try:
                    self.port = input("Port du serveur : ")
                    self.hote = input("Adresse du serveur : ")
                    if self.port == "":
                        self.port = 40000
                    else:
                        self.port = int(self.port)
                    if self.hote == "":
                        self.hote = "localhost"
                    break

                except ValueError:
                    print("Erreur : numero de port invalide.")


            self.connexion = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            try:
                self.connexion.connect((self.hote, self.port))
                print("Info : connexion établie avec le serveur ({}) sur le port({})".format(self.hote,self.port))
                return
            except socket.error:
                print("Erreur : impossible de se connecter au serveur.")

    #se charge de la communication avec le serveur
    def communiquer(self):
        message_reçu = self.connexion.recv(1024).decode()
        if "ask." in message_reçu:
            message_reçu = message_reçu.replace("ask.", "")
            reponse = input(message_reçu)
            try:
                self.connexion.send(bytes(reponse, 'utf-8'))
            except ConnectionResetError:
                pass
        elif "end." in message_reçu:
            self.fermer()
        else:
            print(message_reçu)


    #se charge de fermer le serveur proprement
    def fermer(self):
        print("Info : Fermeture de la connexion")
        self.connexion.close()
        print("Info : Connexion interrompue")


serveur = serveur()
serveur.connecter()
serveur.communiquer()
serveur.fermer()

