class HashMap:
    
    def __init__(self, size):
        self.buckets = [[] for i in range(size)]
        self.size = size
    
    def __str__(self): # transformation du contenu de la hashmap en string pour l'afficher
        string = ""
        for i in range(self.size):
            for y in range(len(self.buckets[i])):
                string = string + self.buckets[i][y][0] + " " + str(self.buckets[i][y][1]) + "/ "
        return string

    def add_key_value(self, key, value, index): # ajout d'un nouveau tuple dans la hashmap (key, value) -> ('username', ChainedList())
        for i in range(len(self.buckets[index])):
            if self.buckets[index][i][0] == key: # si le tuple existe déjà, on le suprimme pour mettre le nouveau
                self.buckets[index].pop(i) # suppression de l'ancien tuple
        self.buckets[index].append((key, value)) # ajout du nouveau tuple
    
    def get(self, key, index): # permet de recupérer la deuxième valeur d'un tuple. Sert à récupérer un historique personnel
        for i in range(len(self.buckets[index])):
            if self.buckets[index][i][0] == key:
                return self.buckets[index][i][1]
        return None
    
    def empty(self, key, value, index): # réinitialisation du deuxième élément d'un tuple
        for i in range(len(self.buckets[index])):
            if self.buckets[index][i][0] == key: # on supprime le tuple en entier
                self.buckets[index].pop(i)
        self.buckets[index].append((key, value)) # puis on ajout le nouveau tuple
    