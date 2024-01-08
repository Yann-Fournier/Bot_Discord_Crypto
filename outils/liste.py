class NodeList: # Noeud de la chaine
    def __init__(self, data, link):
        self.data = data
        self.next_node = link
    
    def add_next(self, node):
        self.next_node = node

class ChainedList: # chaine de noeud
    def __init__(self):
        self.first_node= None
        self.length = 0
    
    def __str__(self): # transforme la liste chainée en string pour l'afficher dans le terminal
        if self.length == 0: # on regarde si l'historique est vide
            return "Vide"
        # Sinon on parcours tous les noeuds de la liste et on ajoute la 'data' à notre chaine de caractère.
        string =  str(self.first_node.data) + ", "
        current_node = self.first_node
        while current_node.next_node is not None:
            string = string + str(current_node.next_node.data) + ", " 
            current_node = current_node.next_node
        return string # on renvoie l'historique transformer en string
    
    def to_str(self): # transforme la liste chainée en string pour l'envoyer sur discord (la mise en page est différente) -> !cmd_user
        if self.length == 0: # on regarde si l'historique est vide
            return "Vide"
        # Sinon on parcours tous les noeuds de la liste et on ajoute la 'data' à notre chaine de caractère.
        string =  str(self.first_node.data) + ",\n"
        current_node = self.first_node
        while current_node.next_node is not None:
            string = string + str(current_node.next_node.data) + ",\n" 
            current_node = current_node.next_node
        return string # on renvoie l'historique transformer en string
    
    def empty(self): # Réinitialisation de la liste chaninée -> vider les historiques
        # réinitialisation des variables de la structure.
        self.first_node = None
        self.length = 0
    
    def len(self): # donne le nombre de noeuds. Longueur de la chaine -> vérification de la longueur de l'historique
        return self.length
        
    def append(self, data): # Ajout d'un nœud à la fin de la liste -> ajout d'une nouvelle commande
        self.length += 1
        current_node = self.first_node
        if current_node is None:
            self.first_node = NodeList(data, None)
            return
        while current_node.next_node is not None:
            current_node = current_node.next_node
        current_node.next_node = NodeList(data, None)
    
# Ces fonctions ne sont pas utilisées --------------------------------------------------------------------------
    def get(self, ind): # cette fonction nous donne la data d'un node précis à l'indice "ind"
        if ind > self.length or ind < 0:
            return
        current_node = self.first_node
        while ind != 0:
            ind -= 1
            current_node = current_node.next_node
        return current_node.data
    
    def search(self, data): # cette fonction nous informe si oui ou non une data éxiste dans la liste
        current_node = self.first_node
        while current_node is not None:
            if current_node.data == data:
                return True
            current_node = current_node.next_node
        return False
    
    def insert(self, ind, data): # insert une data à un indice précis
        if ind > self.length or ind < 0:
            return
        self.length += 1
        if ind == 0:
            seconde_node = self.first_node
            self.first_node = NodeList(data, seconde_node)
            return
        previous_node = self.first_node
        current_node = self.first_node.next_node
        while ind != 1:
            ind -= 1
            previous_node = current_node
            current_node = current_node.next_node
        previous_node.next_node = NodeList(data, current_node)
        
    def remove(self, ind): # supprime le node à l'indice "ind"
        if ind > self.length or ind < 0:
            return
        self.length -= 1
        if ind == 0:
            self.first_node = self.first_node.next_node
        current_node = self.first_node.next_node
        previous_node = self.first_node
        next_node = self.first_node.next_node
        while ind != 0:
            ind -= 1
            previous_node = current_node
            current_node = current_node.next_node
            next_node = current_node.next_node
        previous_node.next_node = next_node