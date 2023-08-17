class Session:

    def __init__(self, debut=None, fin=None, formation=None):
        self.debut = debut
        self.fin=fin
        self.foyers = []
        self.formation = formation