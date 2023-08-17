class Equipe:
    tout = []

    def __init__(self, conseiller=None, nom="", secteur=None):
        self.conseiller = conseiller
        self.participations = []
        self.nom = nom
        self.secteur = secteur
        if nom not in [e.nom for e in Equipe.tout] and nom != "":
            Equipe.tout.append(self)

    def getEquipe(nom=""):
        if nom == "":
            raise Exception("Impossible de trouver d'équipe avec un nom vide")
        if nom not in [e.nom for e in Equipe.tout]:
            e = Equipe(nom=nom)
        else:
            for e in Equipe.tout:
                if e.nom == nom:
                    return e