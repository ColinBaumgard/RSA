import time
import math
import os

os.chdir("D:/User/Bibliothèque/Documents/Python Projects/files")
#os.chdir("/home/serveur/Documents/Python/")
#os.chdir("E:/Python")

#opération sur les fichiers : check;dernier;ecrire,suite
def fichier(retourner = "check", suite = 0):

    nb_ligne = 1 #valeur qui contient le nb de lignes de file_premier.prm
    dernier = 1 #valeur qui contient le dernier nombre de file_premier.prm
    nb_info = 0 #valeur qui contient le nb de lignes de file_info.prm
    dernier_info = 0 #valeur qui contient le dernier nombre de file_info.prm
    info_no = True #True si pas ok



    # On regarde ce qu'on demande :
    if retourner == "dernier":
        if os.path.isfile("file_info.prm"): #si file_info.prm existe :
            with open("file_info.prm", "r") as file_info: #on essaye de l'ouvrir
                nb_info = eval(file_info.readline().rstrip('\n\r'))
                return eval(file_info.readline().rstrip('\n\r'))
        else:
            print("** Erreur : file_info.prm **")

    elif retourner == "ecrire":
        if os.path.isfile("file_info.prm"): #si file_info.prm existe :
            with open("file_info.prm", "r") as file_info: #on essaye de l'ouvrir
                nb_info = eval(file_info.readline().rstrip('\n\r'))
        else:
            print("** Erreur : file_info.prm **")

        if os.path.isfile("file_premiers.prm"): #si file_info.prm existe :
            with open("file_premiers.prm", "a") as file_premiers:
                i = 0
                while i < len(suite):
                    print(suite[i], file=file_premiers)
                    i = i + 1
            with open("file_info.prm", "w") as file_info:
                print(len(suite) + nb_info, file=file_info)
                print(suite[-1], file=file_info)
        else:
            print("** Erreur : file_premeirs.prm **")


    elif retourner == "check":

        if os.path.isfile("file_info.prm"): #si file_info.prm existe :
            with open("file_info.prm", "r") as file_info: #on essaye de l'ouvrir
                nb_info = eval(file_info.readline().rstrip('\n\r'))
                dernier_info = eval(file_info.readline().rstrip('\n\r'))

        else:
            print("** Creation de : file_info.prm **")
            open("file_info.prm", "w")

        if os.path.isfile("file_premiers.prm"): #si filepremier.prm existe :
            with open("file_premiers.prm", "r") as file_premiers: #on essaye de l'ouvrir
                for ligne in file_premiers: #on parcour ses lignes
                    dernier = eval(ligne.rstrip('\n\r'))
                    nb_ligne = nb_ligne+1
        else:
            print("** Creation de : file_premiers.prm **")
            open("file_premiers.prm", "w")

        if nb_info != nb_ligne or dernier_info != dernier : #si il ne correspond pas
            print("** Correction de : file_info.prm **")

        else : #sinon si ils correspondent
            info_no = False #fichiers ok
            print("** Les fichiers sont OK **")

        if info_no: #si fichier pas ok
            with open("file_info.prm", "w") as file_info: #on essaye de l'ouvrir
                print(nb_ligne, file=file_info)
                print(dernier, file=file_info)
                info_no = False

    else:
        print("** Erreur de code ! Mauvaix paramètre à fichier : ** ")

#Lancement de l'algorithme de nombre premier
def creer_nombres_premier(x):
    suite_premiers = []
    i = fichier("dernier") + 1 #on regarde le dernier nombre du fichier on fait + 1 pour ne pas avoir à le rechercher
    k = 0 #compteur nombres premiers total
    j = 0 #compteur %

    print("Calcul à : 0 % ; dernier nombre ecrit : ", i - 1) # on affiche le 0%

    while k <= x:
        if est_premier(i) == 1:
            suite_premiers.append(i)
            k = k + 1
            y = (k/x)*100
            if y > j + 10 :
                j = j + 10
                dernier_ecrit = suite_premiers[-1]
                print("Calcul à :", j, "% ; dernier nombre ecrit : ", dernier_ecrit) # on affiche le %
                fichier("ecrire", suite_premiers)
                suite_premiers = []
        i += 1

#calcul si x est premier (1) ou non (0)
def est_premier(x):
    i = 2
    while i <= math.sqrt(x):
        if x % i == 0:
            return 0
        i = i + 1

    return 1



fichier("check") #On verifie que les fichiers existent et qu'ils correspondent.

choix = "y" #choix de continuer ou non de l'utilisateur
while 1:

    creer_nombres_premier(eval(input("Combien de nouveaux nombres premiers ? : "))) #on creer x nombres premiers

    choix = input("Voulez vous continuer (y/n/check) : ") #On demeande si l'utilisateur veux continuer, checker ou exit
    if choix == "check": # si check : check_same
        fichier("check")
    elif choix != "y": #sinon i != y on exit
        break

