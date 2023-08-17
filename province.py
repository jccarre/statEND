class Province:
    tout = []
    def __init__(self, nom=""):
        self.regions = []
        self.nom = nom
        if nom not in [p.nom for p in Province.tout]:
            Province.tout.append(self)

    def interpreterLigneCSV(dico):
        p = Province(nom=dico["Province"])