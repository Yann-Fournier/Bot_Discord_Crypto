class NodeBinaryTree :
    def __init__(self,data):
        self.data = data
        self.right_child = None
        self.left_child = None
    
    def add_node(self,data):
        if data < self.data:
            if self.left_child is None:
                self.left_child = NodeBinaryTree(data)
            else:
                self.left_child.add_node(data)
        else:
            if self.right_child is None:
                self.right_child = NodeBinaryTree(data)
            else:
                self.right_child.add_node(data)

class BinaryTree:
    def __init__(self):
        self.first_node = None
        self.current_node = self.first_node
          
    def add_data(self, data):
        if self.first_node is None:
            self.first_node = NodeBinaryTree(data)
        else:
            self.first_node.add_node(data)
    
    def get_question(self):
        return self.current_node.data
    
    def send_answer(self, answer):
        if answer == "oui":
            self.current_node = self.current_node.right_node
            return self.current_node.data


# ----------------------------------------------------------------------------------------

class NodeTree:
    def __init__(self, data):
        self.data = data
        self.next_nodes = {}
        
    def add_node(self, question, rep, data): # récursion
        if data == question:
            self.next_nodes[rep] = NodeTree(data)
        else:
            for key, value in self.next_nodes: # car next_nodes est un dictionnaire.
                value.add_node(question, rep, data)
                
    def search(self, data): # récursion
        if data == self.data:
            return True
        else:
            for key, value in self.next_nodes:
                value.search(data)

class Tree:
    def __init__(self):
        self.first_node = None
    
    def add_node(self, question, rep, data):
        if self.first_node is None:
            self.first_node = NodeTree(data)
        else:
            self.first_node.add_node(question, rep, data)
    
    def search(self, data):
        if self.first_node is None:
          return False
        else :
          result = self.first_node.search(data)
          if result is None:
            return False
          else:
            return True