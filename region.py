class Region:
    tout = []
    def __init__(self, nom="", province=None):
        self.secteurs = []
        self.nom = nom
        self.province = province
        if nom not in [r.nom for r in Region.tout]:
            Region.tout.append(self)

    def interpreterLigneCSV(dico):
        p = Region(nom=dico["Région"], province=dico["Province"])