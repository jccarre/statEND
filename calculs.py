from datetime import datetime, date
from tkinter import messagebox

from log import readCSV, logCSV
from os import listdir as osListdir
from os import path as osPath

from province import Province
from region import Region
from secteur import Secteur

import re

import traceback


def appliquerCalculAZones(fonctionRemplissage, nomFichier, est_grandeur_intensive=True):
    """Fonction générique qui applique la fonction permettant de calculer une certaine grandeur (ex:nombre moyen de foyer par équipe) sur tous les secteurs.
    On distingue deux cas spécifiques : les grandeurs extensives comme le nombre total de foyers des grandeurs intensives comme l'age moyen.
    La différence entre ces deux modes concerne le mode de calcul pour les regroupements de secteurs : pour une région, doit-on faire la moyenne de tous les secteurs qui la composent (intensif) ou bien la somme (extensif)."""
    noms_secteurs = {s.nom for s in Secteur.tout}
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
        reader = readCSV(osPath.join("Foyers", annee))

        # On vérifie que le fichier CSV utilise bien le point-virgule comme délimiteur de champ
        nb_colonnes_par_ligne = sum([len(ligne.keys()) for ligne in reader])/len(reader)
        if nb_colonnes_par_ligne < 5:
            messagebox.showwarning("Attention",
                                   "Ce script nécessite l'utilisation de point-virgule comme séparateur de champ dans les fichiers CSV.\nIl semble que le fichier " + annee + " utilise un autre type de séparateur, qui n'est pas accepté.\n\nCe fichier sera donc ignoré.")
            continue
        annee = annee.split(".")[0]
        dico = {}
        dico["année"] = annee
        for secteur in noms_secteurs:
            try:
                dico[secteur] = fonctionRemplissage(secteur, reader, annee)
            except KeyError as e:
                raise Exception("Impossible de trouver la colonne " + str(e) + " dans le fichier " + annee + ".csv")

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

def nbFoyers():
    def f(secteur, reader, *t, **d):
        return len({f["Identifiant"] for f in reader if f["Secteur"] == secteur})
    appliquerCalculAZones(f, "nbFoyers", est_grandeur_intensive=False)


def nbEquipes():
    def f(secteur, reader, *t, **d):
        return len({l["Nom de l'équipe"] for l in reader if l["Secteur"] == secteur})
    appliquerCalculAZones(f, "nbEquipes", est_grandeur_intensive=False)


def ecrire_entete_CSV(nomFichier, noms_secteurs):
    with open(nomFichier, 'w') as filout:
        entete = "année"
        for secteur in noms_secteurs:
            entete += ";" + secteur
        filout.write(entete + "\n")




