from log import readCSV

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
#from foyer import Foyer
from secteur import Secteur
from region import Region
from province import Province
from os import listdir as osListdir
from os import path as osPath
from plotter import generer_image

from calculs import nbFoyerParEquipe, ageMoyen, nbFoyers, nbEquipes

class appli:

    def __init__(self):
        self.actionARealiser = None
        self.nomFichierCouples = ""
        self.fichier_conseillers = ""
        self.fichier_geographie = ""
        self.win = tk.Tk()
        self.win.geometry("1000x400")
        frame_haut = tk.Frame(self.win)
        self.frameCheckBoxZones = tk.Frame(self.win)
        frame_haut.grid(row=0)
        self.frameCheckBoxZones.grid(row=1)
        self.boutonFichierGeographie = ttk.Button(frame_haut, text="Ouvrir fichier provinces-régions-secteurs", command=self.chargerGeographie)
        self.labelFichierGeographie = tk.Label(frame_haut, text="Aucun fichier sélectionné", font='Helvetica 10')
        self.boutonFichierConseillers = ttk.Button(frame_haut, text="Ouvrir fichier conseillers", command=self.chargerConseillers)
        self.labelFichierConseillers = tk.Label(frame_haut, text="Aucun fichier sélectionné", font='Helvetica 10')
        self.boutonFichierCouples = ttk.Button(frame_haut, text="Charger couples", command=self.chargerCouples)
        self.labelFichierCouples = tk.Label(frame_haut, text="Aucun fichier sélectionné", font='Helvetica 10')

        self.choixActions = {"nombre moyen de foyers par équipe":(osPath.join("temp","nbFoyerParEquipe.csv"), nbFoyerParEquipe),
                             "age moyen": (osPath.join("temp","ageMoyen.csv"), ageMoyen),
                             "nombre de foyers":(osPath.join("temp","nbFoyers.csv"), nbFoyers),
                             "nombre d'équipes":(osPath.join("temp","nbEquipes.csv"), nbEquipes)}
        self.combobox = ttk.Combobox(frame_haut, values=[a for a in self.choixActions.keys()], width=30)
        self.combobox.set("Choisir une grandeur à afficher")
        self.combobox.bind("<<ComboboxSelected>>", self.on_selection)
        self.combobox["state"] = "disabled"

        self.boutonGenererGraphe = ttk.Button(frame_haut, text="Générer graphe", command=self.genererGraphe)
        self.boutonGenererGraphe["state"] = "disabled"


        self.checkboxVar = {}

        self.boutonFichierGeographie.grid(row=0, column=0, padx=30, pady=30)
        self.labelFichierGeographie.grid(row=0, column=1)
        #self.boutonFichierConseillers.grid(row=1, column=0)
        #self.labelFichierConseillers.grid(row=1, column=1)
        #self.boutonFichierCouples.grid(row=2, column=0)
        #self.labelFichierCouples.grid(row=2, column=1)
        self.combobox.grid(row=0,column=3, padx=30)
        self.boutonGenererGraphe.grid(row=1, column=3, padx=30)


        self.listeZoneAAfficher = []

        self.frameCheckBoxSecteurs = tk.Frame(self.frameCheckBoxZones)
        self.frameCheckBoxRegions = tk.Frame(self.frameCheckBoxZones)
        self.frameCheckBoxProvinces = tk.Frame(self.frameCheckBoxZones)
        labelsecteurs = tk.Label(self.frameCheckBoxZones, text="Secteurs", font='Helvetica 10')
        labelsecteurs.grid(row=0, column=0, padx=15, pady=15)
        labelregions = tk.Label(self.frameCheckBoxZones, text="Regions", font='Helvetica 10')
        labelregions.grid(row=1, column=0, padx=15, pady=15)
        labelprovinces = tk.Label(self.frameCheckBoxZones, text="Provinces", font='Helvetica 10')
        labelprovinces.grid(row=2, column=0, padx=15, pady=15)
        self.frameCheckBoxSecteurs.grid(row=0, column=1, padx=15, pady=15)
        self.frameCheckBoxRegions.grid(row=1, column=1, padx=15, pady=15)
        self.frameCheckBoxProvinces.grid(row=2, column=1, padx=15, pady=15)
        self.checkboxZone = {}


        self.win.mainloop()

    def genererGraphe(self):
        try:
            if not self.listeZoneAAfficher:
                raise Exception("Veuillez sélectionner au moint une zone géographique (secteur, région ou province) à analyser")
            self.actionARealiser()
            generer_image(fichier=self.fichierATracer, columns=self.listeZoneAAfficher)
        except Exception as e:
            messagebox.showwarning("Attention",
                                   "Erreur : " + "\n" + str(e))

    def on_selection(self, event):
        selected_item = self.combobox.get()
        self.actionARealiser = self.choixActions[selected_item][1]
        self.fichierATracer = self.choixActions[selected_item][0]
        if str(self.boutonGenererGraphe["state"]) == "disabled":
            self.boutonGenererGraphe["state"] = "enabled"

    def on_checkbox_click(self):
        self.listeZoneAAfficher.clear()
        for nomZone in [s.nom for s in Secteur.tout] + [r.nom for r in Region.tout] + [p.nom for p in Province.tout]:
            if self.checkboxVar[nomZone].get():
                self.listeZoneAAfficher.append(nomZone)
        print(self.listeZoneAAfficher)

    def chargerGeographie(self):
        self.fichier_geographie = fd.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        reader = readCSV(self.fichier_geographie)
        for ligne in reader :
            Secteur.interpreterLigneCSV(ligne)
            Region.interpreterLigneCSV(ligne)
            Province.interpreterLigneCSV(ligne)

        self.remplirCheckBoxZone(Secteur.tout, self.frameCheckBoxSecteurs)
        self.remplirCheckBoxZone(Region.tout, self.frameCheckBoxRegions)
        self.remplirCheckBoxZone(Province.tout, self.frameCheckBoxProvinces)

        nbSecteurs = str(len(Secteur.tout))
        nbRegions = str(len(Region.tout))
        nbProvince = str(len(Province.tout))
        message = nbSecteurs + " secteurs    |    " + nbRegions + " régions    |    " + nbProvince + " provinces"
        self.labelFichierGeographie.config(text=message)
        self.combobox["state"] = "enabled"

    def remplirCheckBoxZone(self, zones, frame):
        numCheckBox = 0
        nomsZones = [s.nom for s in zones]
        nomsZones.sort(key=len)
        nbLignes = max((len(zones)//6), 1)
        for nomZone in nomsZones:
            self.checkboxVar[nomZone] = tk.BooleanVar()
            self.checkboxZone[nomZone] = tk.Checkbutton(frame, text=nomZone,
                                                        variable=self.checkboxVar[nomZone],
                                                        command=self.on_checkbox_click)
            self.checkboxZone[nomZone].grid(row=numCheckBox % nbLignes, column=numCheckBox // nbLignes, sticky="w", padx=0, pady=0)
            numCheckBox += 1

    def chargerConseillers(self):
        self.fichier_conseillers = fd.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        reader = readCSV(self.fichier_conseillers)
        self.labelFichierConseillers.config(text=self.fichier_conseillers)

    def chargerCouples(self):
        if not Secteur.tout:
            messagebox.showwarning("Attention", "Aucun secteur en mémoire.\nVeuillez commencer par charger le fichier de géographie (répartition des secteurs par régions et provinces)")
            return
        for annee in osListdir("Foyers"):
            reader = readCSV(osPath.join("Foyers", annee))
            numLigne = 1
            for ligne in reader :
                numLigne += 1
                try:
                    Foyer.interpreterLigneCSV(ligne, annee)
                except KeyError as e:
                    messagebox.showwarning("Attention",
                                           "Erreur lors du chargement de " + str(annee) + " à la ligne " + str(numLigne) + "\n\nImpossible de trouver la colonne " + str(e))
                    return
                except Exception as e:
                    messagebox.showwarning("Attention",
                                           "Erreur lors du chargement de " + str(annee) + " à la ligne " + str(numLigne) + "\n\n" + str(e))
                    return
            self.labelFichierCouples.configure(text=self.nomFichierCouples)

appli()
