import random
class RandomizedSet:

    def __init__(self):
        self.hash_table = dict()
        self.lst = []
    def insert(self, val: int) -> bool:
        if val not in self.hash_table:
            self.hash_table[val] = len(self.lst)
            self.lst.append(val)
            return True
        else:
            return False
    def remove(self, val: int) -> bool:
        if val in self.hash_table:
            idx = self.hash_table.pop(val)
            # swap if index is not last
            if idx != len(self.lst)-1:
                last = self.lst[-1]
                self.lst[-1] = self.lst[idx]
                self.lst[idx] = last
                self.hash_table[last] = idx
            self.lst.pop()
            return True
        else:
            return False
    def getRandom(self) -> int:
        if not self.lst:
            raise IndexError("getRandom() called on empty set")
        return self.lst[random.randint(0, len(self.lst) - 1)]