from datetime import datetime

from personne import Personne
from equipe import Equipe
from secteur import Secteur


class Foyer:
    tout = []
    def __init__(self,
                 id=-1,
                 pays=None,
                 lui=None,
                 elle=None,
                 nom="",
                 telFixe="",
                 email="",
                 autreEmail="",
                 adresse="",
                 codePostal="",
                 commune="",
                 dateMariage=None,
                 equipe=""):
        self.id = id
        self.lui = lui
        self.elle = elle
        self.dateDebutEND = None
        self.nom = nom
        self.telFixe = telFixe
        self.email = email
        self.autreEmail = autreEmail
        self.adresse = adresse
        self.codePostal = codePostal
        self.commune = commune
        if dateMariage is not None and dateMariage != "":
            self.dateMariage = datetime.strptime(dateMariage, "%d/%m/%Y").date()
        self.enfants = []
        self.sessions = []
        self.participations = []
        self.mandats = []
        self.equipe = Equipe.getEquipe(nom=equipe)
        if id not in [f.id for f in Foyer.tout]:
            Foyer.tout.append(self)

    def interpreterLigneCSV(dico, annee):
        if len(dico.keys()) < 10:
            raise Exception("Impossible de distinguer les colonnes dans le fichier.\n\nVérifier que le point-virgule est utilisé comme séparateur de champs")
        if dico["Identifiant"] not in [f.id for f in Foyer.tout]:
            lui = Personne(prenom=dico["Prenom LUI"],
                           sexe=False,
                           dateDeNaissance=dico["Date de naissance LUI"],
                           portable=dico["Mobile LUI"],
                           profession=dico["Profession LUI"],
                           annee=annee)
                           # nationalite=dico["Nationalite LUI"],
                           # mobileListeRouge=(dico["Mobile LUI liste rouge"] == "Oui"),
                           # dateDeces=dico["Date de décès LUI"],
                           # retraite=(dico["Retraite LUI"] == "Oui"))
            elle = Personne(prenom=dico["Prenom ELLE"],
                            sexe=True,
                            dateDeNaissance=dico["Date de naissance ELLE"],
                            portable=dico["Mobile ELLE"],
                            profession=dico["Profession ELLE"],
                            annee=annee)
                            # nationalite=dico["Nationalite ELLE"],
                            # mobileListeRouge=(dico["Mobile ELLE liste rouge"] == "Oui"),
                            # dateDeces=dico["Date de décès ELLE"],
                            # retraite=(dico["Retraite ELLE"] == "Oui"))
            secteur = Secteur.getSecteur(nom=dico["Secteur"])
            equipe = Equipe(nom=dico["Nom de l'équipe"], secteur=secteur)
            f = Foyer(id=dico["Identifiant"],
                      pays=dico["Pays"],
                      lui=lui,
                      elle=elle,
                      nom=dico["Nom"],
                      telFixe=dico["Téléphone"],
                      codePostal=dico["Code postal"],
                      commune=dico["Commune"],
                      dateMariage=dico["Date de mariage"],
                      equipe=dico["Nom de l'équipe"])
                      # email=dico["Email"],
                      # autreEmail=dico["Autre email"],
                      # adresse=dico["Adresse"],

            #  "Identifiant"\
            #  "Nom foyer"
            #  "Nom" \
            #  "Prenom LUI"\
            #  "Prenom ELLE"
            #  "Email"\
            #  "Nom de l'équipe"\
            #  "Secteur"\
            #  "Adresse"\
            #  "Complément"\
            #  "Code postal"\
            #  "Commune"\
            #  "Pays"\
            #  "Autre email"\
            #  "Téléphone"\
            #  "Téléphone liste rouge"\
            #  "Mobile LUI"\
            #  "Mobile LUI liste rouge"\
            #  "Mobile ELLE"\
            #  "Mobile ELLE liste rouge"\
            #  "Date de naissance LUI"\
            #  "Date de naissance ELLE"\
            #  "Date de mariage"\
            #  "Date de décès LUI"\
            #  "Date de décès ELLE"\
            #  "Date entrée aux END"\
            #  "Nationalite LUI"\
            #  "Nationalite ELLE"\
            #  "Profession LUI"\
            #  "Profession ELLE"\
            #  "Retraite LUI"\
            #  "Retraite ELLE"\
            #  "Engagement 1 LUI"\
            #  "Engagement 2 LUI"\
            #  "Engagement 1 ELLE"\
            #  "Engagement 2 ELLE"\
            #  "Equipe Responsable"\
            #  "Foyer Informateur"\
            #  "Foyer Liaison"\
            #  "Foyer Pilote"\
            #  "Paroisse fréquentée"\
            #  "Masqués dans annuaire"\
            #  "Enfants"\
            #  "Date entrée équipe"\
            #  "Formations"