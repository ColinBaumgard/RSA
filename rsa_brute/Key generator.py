import os
import random

os.chdir("D:/User/Bibliothèque/Documents/Programmes/Python Projects/RSA/files")
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
        while i < k : #Code le message en Ascii
            messageA.append(chr(message[i]))
            i += 1

    else:
        while i < k : #Decode le message en Ascii
            messageA.append(ord(message[i]))
            i += 1

    return messageA

#Crypte une suite de caractère
def rsa(message_ascii, e_ou_d, n):
    k = len(message_ascii)
    i = 0
    message_B = []

    while i < k:
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





p,q = nombre_premiers()
n = p*q
phi = (p-1)*(q-1)
e = premier_avec(phi, plus_grand(p,q))
d = invmod(e, phi)

print("--> Cle publique : (",e,",",n,")")
print("--> Cle privée   : (",d,",",n,")")

message_ascii = ascii(input("Entrez le mot ou la phrase à crypter : "), "ascii") #mot = ascci

message_crypte = rsa(message_ascii, e, n)
message_decrypte_ascii = rsa(message_crypte, d, n)
message_decrypte = ascii(message_decrypte_ascii, "back")

print("message crypté : ", message_crypte)
