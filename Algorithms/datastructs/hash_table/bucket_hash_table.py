"""
bucket_hash_table.py
Design a data structure to store the strings' counts 
with the ability to return the strings with minimum and maximum counts.
"""

class Bucket:
    def __init__(self, count):
        self.count = count
        self.keys = set()
        self.prev = None
        self.next = None
    def __repr__(self):
        res = "Count: " + str(self.count) + "\n"
        res += "Keys: " + str(self.keys) + "\n"
        res += "Previous Bucket None: " + str(self.prev is None) + "\n"
        res += "Next Bucket None: " + str(self.next is None) + "\n"
        return res
# don't store a flat doubly linked list because may have worst case O(n)
# duplicate keys with the same count
class AllOne:
    def __init__(self):
        self.key_to_bucket = dict()
        self.start = Bucket(0)
        self.end = Bucket(0)
        self.start.next = self.end
        self.end.prev = self.start

    def inc(self, key: str) -> None:
        if key not in self.key_to_bucket:
            if self.start.next != self.end and self.start.next.count == 1:
                self.key_to_bucket[key] = self.start.next
                self.start.next.keys.add(key)
            else:
                # bucket of one not added at start
                b = Bucket(1)
                b.keys.add(key)
                old_first = self.start.next
                self.start.next = b
                b.prev = self.start

                b.next = old_first
                old_first.prev = b
                self.key_to_bucket[key] = b
        else:
            # increment existing key in bucket
            bucket = self.key_to_bucket[key]
            bucket.keys.remove(key)
            inc_count = bucket.count+1
            old_next = bucket.next
            old_prev = bucket.prev
            if old_next != self.end and old_next.count == inc_count:
                dest = old_next
            else:
                # add a new bucket with count
                dest = Bucket(count=inc_count)
                dest.next = old_next
                dest.prev = bucket

                old_next.prev = dest
                bucket.next = dest
            dest.keys.add(key)
            self.key_to_bucket[key] = dest

            if not bucket.keys:
                bucket.next.prev = bucket.prev
                bucket.prev.next = bucket.next
                

    def dec(self, key: str) -> None:
        bucket = self.key_to_bucket[key]
        bucket.keys.remove(key)
        dec_count = bucket.count-1
        old_prev = bucket.prev
        old_next = bucket.next
        if dec_count == 0:
            del self.key_to_bucket[key]
        else:
            if old_prev != self.start and dec_count == old_prev.count:
                dest = old_prev
            else:
                dest = Bucket(dec_count)
                dest.prev = old_prev
                dest.next = bucket

                old_prev.next = dest
                bucket.prev = dest
    
            dest.keys.add(key)
            self.key_to_bucket[key] = dest
        if not bucket.keys:
            bucket.next.prev = bucket.prev
            bucket.prev.next = bucket.next

    def getMaxKey(self) -> str:
        if self.end.prev == self.start:
            return ""
        else:
            return next(iter(self.end.prev.keys))

    def getMinKey(self) -> str:
        if self.start.next == self.end:
            return ""
        else:
            return next(iter(self.start.next.keys))