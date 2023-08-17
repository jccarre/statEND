from datetime import date, datetime
class Personne:
    tout = {}
    dernierId = 0
    def __init__(self,
                 prenom="",
                 sexe=False,
                 dateDeNaissance=None,
                 nationalite="",
                 portable="",
                 profession=None,
                 mobileListeRouge=False,
                 dateDeces=None,
                 retraite=False,
                 annee=0):
        if annee == 0:
            raise Exception("Il faut renseigner l'année lors de la création d'une personne")
        self.id = Personne.dernierId
        Personne.dernierId += 1
        self.prenom = prenom
        self.sexe = sexe #False pour un homme
        if dateDeNaissance is not None and dateDeNaissance != "":
            self.dateDeNaissance = datetime.strptime(dateDeNaissance, "%d/%m/%Y").date()
        self.retraite = retraite
        self.nationalite = nationalite
        self.portable = portable
        self.profession = profession
        self.mobileListeRouge = mobileListeRouge
        if dateDeces is not None and dateDeces != "":
            self.dateDeces = datetime.strptime(dateDeces, "%d/%m/%Y").date()
        Personne.tout[annee].append(self)


    def age(self):
        current_date = date.today()
        return current_date.year - self.dateDeNaissance.year - ((current_date.month, current_date.day) < (self.dateDeNaissance.month, self.dateDeNaissance.day))