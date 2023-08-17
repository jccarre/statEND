class Secteur:
    tout = []
    def __init__(self, nom="", region=None, province=None):
        self.mandats=[]
        self.equipes = []
        self.nom = nom
        self.region = region
        self.province = province
        if nom not in [s.nom for s in Secteur.tout]:
            Secteur.tout.append(self)

    def interpreterLigneCSV(dico):
        s = Secteur(nom=dico["Secteur"], region=dico["Région"], province=dico["Province"])

    def getSecteur(nom=""):
        if nom == "":
            return None
        if nom not in [s.nom for s in Secteur.tout]:
            raise Exception("Le secteur " + nom + " ne figure pas dans la liste des secteurs.")
        else:
            return [s for s in Secteur.tout if s.nom == nom][0]