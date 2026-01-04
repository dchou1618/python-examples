import functools

class Node(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class NodeList:
    def __init__(self):
        self.start = None
        self.end = None
    def add(self, key: int, value: int):
        temp = Node(key, value)
        if self.start:
            if self.start == self.end:
                self.start.next = temp
                self.end = temp
                self.end.prev = self.start
            else:
                temp.prev = self.end
                self.end.next = temp
                self.end = temp
        else:
            self.start = temp
            self.end = self.start
        return temp
    def remove(self, node: Node):
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        else:
            self.start = next_node
        if next_node:
            next_node.prev = prev_node
        else:
            self.end = prev_node
    def move_to_end(self, node):
        if node == self.end:
            return
        self.remove(node)
        node.prev = self.end
        node.next = None
        self.end.next = node
        self.end = node
    def evict(self):
        start = self.start
        if not start:
            return None
        next_node = start.next
        if next_node:
            next_node.prev = None
            self.start = next_node
        else:
            self.start = None
            self.end = None
        return start
    def __str__(self):
        head = self.start
        res = ""
        while head:
            res += f"Node(key: {head.key}, value: {head.value}, prev: {head.prev}, next: {head.next})"
            head = head.next
        return res

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.table = dict()
        self.cache = NodeList()
    def get(self, key: int) -> int:
        if key in self.table:
            node = self.table[key]
            self.cache.move_to_end(node)
            return node.value
        else:
            return -1
    def put(self, key: int, value: int) -> None:
        if key in self.table:
            old_node = self.table[key]
            old_node.value = value
            self.cache.move_to_end(old_node)
        else:
            if self.capacity == 0:
                return
            if len(self.table) == self.capacity:
                lru = self.cache.evict()
                del self.table[lru.key]
                node = self.cache.add(key, value)
                self.table[key] = node
            else:
                node = self.cache.add(key, value)
                self.table[key] = node

# using the functools cache decorator
@functools.lru_cache
def factorial(n: int) -> int:
    return n*factorial(n-1) if n > 1 else 1