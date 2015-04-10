import os
import random

os.chdir("D:/User/Bibliothèque/Documents/Python Projects/files")
#os.chdir("/home/serveur/Documents/Python/")
#os.chdir("E:/Python")

#retourne un nombre premier tiré du fichier file_premiers.prm
def nombre_premiers():

    i = 0
    nb_info = 0
    retour = []
    suite_premiers = []

    if os.path.isfile("file_info.prm"):
        with open("file_info.prm", "r") as file_info:
            nb_info = eval(file_info.readline().rstrip('\n\r'))
            au_pif = random.randrange(0 ,nb_info)

    if os.path.isfile("file_premiers.prm"):
        with open("file_premiers.prm", "r") as file_premiers:
            for ligne in file_premiers: #on parcour ses lignes
                if au_pif == i :
                    retour.append(eval(ligne.rstrip('\n\r')))
                    if len(retour) == 2 :
                        return retour[0], retour[1]
                    au_pif = random.randrange(i ,nb_info)
                i = i + 1

    print("** Fichier manquant : file_premiers/info ; Veuillez lancer le programme : Prem's generator.py **")
    return 0,0

#retourne le plus grand de a et b
def plus_grand(a,b):
    if a > b :
        return a
    else:
        return b

#retourne e premier avec phi tel que : p,q < e < phi
def premier_avec(phi, a):
    e = a + 1 # on commence à a + 1 pour p,q < e

    while pgcd(e, phi) != 1: #tant que pas premier, e = e + 1
        e = e + 1

    if e < phi : # on verifie bien que e < phi
        return e
    else :
        print("** Erreur : aucun e possible ! **")
        return 0

#fonction qui calcul le pgcd de deux nombres
def pgcd(a, b):
    while 1:
        r = a % b
        if r == 0 :
             return b
        a = b
        b = r

#Code (sens = "ascci") et decode (sens != "ascci") en ascii
def ascii(message, sens = "ascii"):
    messageA = []
    k = len(message)
    i = 0

    if sens != "ascii":
        while i < k : #ascii -> caractère
            messageA.append(chr(message[i]))
            i += 1

    else:
        while i < k : #caractère -> ascii
            messageA.append(ord(message[i]))
            i += 1

    return messageA

#Crypte une suite de caractère
def rsa(message_ascii, e_ou_d, n):
    k = len(message_ascii)
    i = 0
    message_B = []

    while i < k:
        if type(message_ascii[i]) is str:
            message_ascii[i] = eval(message_ascii[i])
        message_B.append(pow(message_ascii[i], e_ou_d, n))
        i = i + 1

    return message_B

#fct récursive qui renvoie (g,x,y) tq ax+by=g (=pgcd(a,b))
def bezout(p,q):
    if p==0:
        return (q,0,1)
    else:
        g,y,x=bezout(q%p,p)
        return (g,x-(q//p)*y,y)

#inverse modulaire de a modulo q
def invmod(e, phi):

    g,x,y=bezout(e,phi)
    if g!=1:
        raise Exception('pas inversible')
    else:
        return x%phi

#demande un int
def demander_int(question): #fonction pour demander
    reponse = input(question)
    return int(reponse)

#creer une paire de clé
def creation_clé():
    p,q = nombre_premiers()
    n = p*q
    phi = (p-1)*(q-1)
    e = premier_avec(phi, plus_grand(p,q))
    d = invmod(e, phi)

    print("--> Cle publique ( e ; n ) : (",e,",",n,")")
    print("--> Cle privée   ( d ; n ) : (",d,",",n,")")

    return e,d,n

#demande une paire de clé
def demander_clé():
    while 1:
        n = eval(input('Veuillez rentrer "n" -> c.pub. ( e ;_n_) : '))
        n = eval(input('Veuillez rentrer "e" -> c.pub. (_e_; n ) : '))
        n = eval(input('Veuillez rentrer "d" -> c.pri. (_d_; n ) : '))
        print("\n--> Cle publique ( e ; n ) : (",e,",",n,")")
        print("--> Cle privée   ( d ; n ) : (",d,",",n,")\n")
        if input("Validez-vous ? (y/n) : ") != "y":
            return e,d,n

def ecrire_message(e,n):
    message_crypte = rsa(ascii(input("Entrez le mot ou la phrase à crypter : "), "ascii"),e,n)
    k = len(message_crypte)
    i = 0
    while i < k :
        message_crypte[i] = str(message_crypte[i])
        i = i + 1
    print(" ".join(message_crypte)) #mot -> ascii -> rsa -> split -> affiche

def lire_message(d,n):
    print("\n\n--> Decryptage du message (fin pour terminer la saisie) :")
    message_decrypte = input("Votre message crypté : ").split(" ")
    message_decrypte = ascii(rsa(message_decrypte, d, n),  "back")
    print("--> Le message decrypté :")
    print("".join(message_decrypte))
    return 0



print("\n********************** RSA **********************\n*                     v.1.0                     *\n*************************************************\n")

clé = input("Avez-vous déjà une paire de clé ? (y/n) : ")
if clé == "y":
    e,d,n = demander_clé()
else :
    e,d,n = creation_clé()


while 1:
    choix = int(input("\n** MENU **\nVous voulez : \n1.Ecrire un message\n2.Dechiffrer un message\n3.Quitter\nVotre choix : "))
    if choix == 1 :
        ecrire_message(e,n)
    elif choix == 2 :
        choix = lire_message(d,n)
    elif choix == 3 :
        input("\nMerci d'avoir utilisé mon programme !\nTapez sur 'entrée' pour quitter\n(c)Colin Baumgard\n")
        break
    else:
        print("Commande invalide")




