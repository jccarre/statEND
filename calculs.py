from datetime import datetime, date
from tkinter import messagebox

from log import readCSV, logCSV, create_file_and_folder
from os import listdir as osListdir
from os import path as osPath

from province import Province
from region import Region
from secteur import Secteur

from chardet import detect as chardetDetect #Pour détecter l'encodage d'un fichier

import re

import traceback

encodage_detecte = "utf-8"


def appliquerCalculAZones(fonctionRemplissage, nomFichier, est_grandeur_intensive=True):
    global encodage_detecte
    """Fonction générique qui applique la fonction permettant de calculer une certaine grandeur (ex:nombre moyen de foyer par équipe) sur tous les secteurs.
    On distingue deux cas spécifiques : les grandeurs extensives comme le nombre total de foyers des grandeurs intensives comme l'age moyen.
    La différence entre ces deux modes concerne le mode de calcul pour les regroupements de secteurs : pour une région, doit-on faire la moyenne de tous les secteurs qui la composent (intensif) ou bien la somme (extensif)."""
    noms_secteurs = {s.nom for s in Secteur.tout}
    create_file_and_folder("temp", nomFichier + ".csv")
    ecrire_entete_CSV(osPath.join("temp", nomFichier + ".csv"), noms_secteurs)
    annees = [annee for annee in osListdir("Foyers")]
    annees.sort()
    if not annees:
        raise Exception("Le dossier 'Foyers' est vide. Il doit contenir les fichiers csv à analyser")
    for annee in annees:
        # On vérifie que le nom du fichier correspond au format attendu.
        pattern = re.compile("^[0-9]+\.csv$")
        if not pattern.match(annee):
            messagebox.showwarning("Attention",
                                   "Le fichier '" + annee + "' a un nom qui ne correspond pas au format attendu pour les fichiers CSV par année.\nOn attend des noms comme '2019.csv' ou '2020.csv'\n\nCe fichier sera ignoré mais la procédure continue.")
            continue
        
        # Une large gamme d'encodage existent en fonction du tableur utilisé et du système d'exploitation. Le paragraphe suivant essaie de détecter l'encodage du fichier CSV.
        reader = None
        try:
            reader = readCSV(osPath.join("Foyers", annee))
        except UnicodeDecodeError as e1:
            try:
                print("Ancien encodage détecté : " + encodage_detecte)
                reader = readCSV(osPath.join("Foyers", annee), encoding=encodage_detecte)
            except UnicodeDecodeError as e:
                print(type(e))
                fichierAlire = osPath.join("Foyers", annee)
                rawdata = open(fichierAlire, "rb").read()
                result = chardetDetect(rawdata)
                encodage_detecte = result['encoding']
                print("Nouvel encodage détecté : " + encodage_detecte)
                try:
                    reader = readCSV(osPath.join("Foyers", annee), encoding=encodage_detecte)
                except UnicodeDecodeError:
                    raise Exception("Impossible de détecter l'encodage utilisé dans le fichier " + fichierAlire + ".\nVeuillez convertir vos fichiers en encodage UTF-8.")
                
        if not verifier_fichier_CSV(reader, annee, ):
            continue
        annee = annee.split(".")[0]
        dico = {}
        dico["année"] = annee
        for secteur in noms_secteurs:
            if secteur not in {l["Secteur"] for l in reader}:
                raise Exception("Le secteur '" + secteur + "' qui apparaît dans la liste des secteurs (fichier de géographie), n'est pas présent dans le fichier " + annee + ".csv\nVeuillez vérifier qu'il est ortographié de la même façon dans les deux fichiers.")
            try:
                dico[secteur] = fonctionRemplissage(secteur, reader, annee)
            except KeyError as e:
                raise Exception("Impossible de trouver la colonne " + str(e) + " dans le fichier " + annee + ".csv")
            except Exception as e:
                print(e)

        for region in Region.tout:
            secteurs = [s.nom for s in Secteur.tout if s.region == region.nom]
            dico[region.nom] = 0
            for s in secteurs:
                dico[region.nom] += dico[s]
            if est_grandeur_intensive:
                dico[region.nom] = dico[region.nom] / len(secteurs)

        for province in Province.tout:
            secteurs = [s.nom for s in Secteur.tout if s.province == province.nom]
            dico[province.nom] = 0
            for s in secteurs:
                dico[province.nom] += dico[s]
            if est_grandeur_intensive:
                dico[province.nom] = dico[province.nom] / len(secteurs)
        
        logCSV(dico, nom_fichier=osPath.join("temp", nomFichier + ".csv"))

def nbFoyerParEquipe():
    def f(secteur, reader, *t, **d):
        noms_equipes = {l["Nom de l'équipe"] for l in reader if l["Secteur"] == secteur}
        nbTotalFoyers = 0
        for equipe in noms_equipes:
            nbFoyers = len([f["Nom foyer"] for f in reader if f["Nom de l'équipe"] == equipe])
            nbTotalFoyers += nbFoyers
        return nbTotalFoyers/len(noms_equipes)

    appliquerCalculAZones(f, "nbFoyerParEquipe")


def ageMoyen():
    def f(secteur, reader, annee, *t, **d):
        def calculAge(dateNaissance, annee):
            dateNai = datetime.strptime(dateNaissance, "%d/%m/%Y").date()
            return int(annee) - dateNai.year

        pattern = re.compile("^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$")
        ages = [calculAge(l["Date de naissance LUI"], annee) for l in reader if l["Secteur"] == secteur and pattern.match(l["Date de naissance LUI"])]
        ages += [calculAge(l["Date de naissance ELLE"], annee) for l in reader if l["Secteur"] == secteur and pattern.match(l["Date de naissance ELLE"])]
        return sum(ages) / len(ages)

    appliquerCalculAZones(f, "ageMoyen")
    print("fin de la fonction ageMoyen")

def nbFoyers():
    def f(secteur, reader, *t, **d):
        return len({f["Identifiant"] for f in reader if f["Secteur"] == secteur})
    appliquerCalculAZones(f, "nbFoyers", est_grandeur_intensive=False)


def nbEquipes():
    def f(secteur, reader, *t, **d):
        return len({l["Nom de l'équipe"] for l in reader if l["Secteur"] == secteur})
    appliquerCalculAZones(f, "nbEquipes", est_grandeur_intensive=False)


def ecrire_entete_CSV(nomFichier, noms_secteurs):
    with open(nomFichier, 'w', encoding='utf-8') as filout:
        entete = "année"
        for secteur in noms_secteurs:
            entete += ";" + secteur
        filout.write(entete + "\n")


def verifier_fichier_CSV(reader, nom_fichier):
    # On vérifie que le fichier CSV utilise bien le point-virgule comme délimiteur de champ
    nb_colonnes_par_ligne = sum([len(ligne.keys()) for ligne in reader]) / len(reader)
    if nb_colonnes_par_ligne < 5:
        messagebox.showwarning("Attention",
                               "Ce script nécessite l'utilisation de point-virgule comme séparateur de champ dans les fichiers CSV.\nIl semble que le fichier " + annee + " utilise un autre type de séparateur, qui n'est pas accepté.\n\nCe fichier sera donc ignoré.")
        return False
    return True

    # On vérifie que tous les secteurs, régions et provinces qui se trouvent dans ce fichier existent dans le fichier dé géographie:
    secteurs_connus = [s.nom for s in Secteur.tout]
    secteurs_manquants = {ligne['Secteur'] for ligne in reader if ligne['Secteur'] not in secteurs_connus}
    secteurs_presents = {ligne['Secteur'] for ligne in reader}
    if secteurs_manquants:
        message = "Le secteur {secteur} qui se trouve dans le fichier {fichier} n'existe pas dans le fichier de géographie.\n" + \
                  "Veuillez vérifier qu'il s'y trouve et qu'il est correctement orthographié"
        message = message.format(secteur=list(secteurs_manquants)[0], fichier=nom_fichier)
        if len(secteurs_manquants) > 1:
            message = "Les secteurs {secteurs} qui se trouve dans le fichier {fichier} n'existent pas dans le fichier de géographie.\n" + \
                      "Veuillez vérifier qu'ils s'y trouvent et qu'il sont correctement orthographiés"
            liste_secteurs = "\n"
            for s in secteurs_manquants:
                liste_secteurs += s + "\n"
            message = message.format(secteurs=liste_secteurs, fichier=nom_fichier)
        messagebox.showwarning("Attention", message)
        return False

