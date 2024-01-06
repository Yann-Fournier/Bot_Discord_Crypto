class HashMap:
    
    def __init__(self, size):
        self.buckets = [[] for i in range(size)]
        self.size = size
    
    def __str__(self):
        string = ""
        for i in range(self.size):
            for y in range(len(self.buckets[i])):
                string = string + self.buckets[i][y][0] + " " + str(self.buckets[i][y][1]) + "/ "
        return string

    def add_key_value(self, key, value, index):
        for i in range(len(self.buckets[index])):
            if self.buckets[index][i][0] == key:
                self.buckets[index].pop(i)
        self.buckets[index].append((key, value))
    
    def get(self, key, index):
        for i in range(len(self.buckets[index])):
            if self.buckets[index][i][0] == key:
                return self.buckets[index][i][1]
        return None
    
    def empty(self, key, value, index):
        for i in range(len(self.buckets[index])):
            if self.buckets[index][i][0] == key:
                self.buckets[index].pop(i)
        self.buckets[index].append((key, value))
    