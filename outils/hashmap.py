class HashMap:
    def __init__(self, size):
        self.buckets = [[] for i in range(size)]
        self.size = size
        
    def add_key_value(self, key, value):
        index = hash(key) % self.size
        for i in range(len(self.buckets[index])):
            if self.buckets[index][i][0] == key:
                self.buckets[index].pop(i)
        self.buckets[index].append((key, value))
    
    def get(self, key):
        index = hash(key) % self.size
        for i in range(len(self.buckets[index])):
            if self.buckets[index][i][0] == key:
                return self.buckets[index][i][1]
        return None
    
    def remove(self, key):
        index = hash(key) % self.size
        for i in range(len(self.buckets[index])):
            if self.buckets[index][i][0] == key:
                self.buckets[index].pop(i)
                return