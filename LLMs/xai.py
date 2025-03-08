from typing import List
import numpy as np
from dataclasses import dataclass

REQUEST_QUEUE = []
VOCAB_SIZE = 10

def lm_batch(prev_tokens: List[List[int]]):
    next_tokens = []
    for sequence in prev_tokens:
        next_tokens.append(hash(tuple(sequence)) % VOCAB_SIZE)
    return next_tokens

    

class ReturnHandle:

    RETURN = dict()
    def __init__(self, key):
        self.key = key
    def return_result(self, sequence: List[int]):
        self.__class__.RETURN[self.key] = sequence

@dataclass
class Request:
    prompt: List[int]
    handle: ReturnHandle


def process_loop(batch_size=8, max_len=20, stop_token=0):
    active = batch_size * [None]
    while True:
        i = 0
        while i < batch_size:
            elem = dequeue()
            if elem:
                active[i] = [elem, np.array([])]
            else:
                break
            i += 1
        print(f"Batch Length: {i}")
        
        if i == 0:
            return
        for iter in range(1,max_len+1):
            contexts = [np.concatenate((val[0].prompt, val[1])) for val in active if val is not None]
            next_tokens = lm_batch(contexts)
            if len(next_tokens) == 0:
                break
            for j in range(len(next_tokens)):
                if active[j]:
                    if next_tokens[j] == stop_token or iter == max_len:
                        print(f"Iter: {iter}: ", next_tokens[j])
                        active[j][0].handle.return_result(active[j][1])
                        active[j] = None
                    else:
                        # print("Before", active[j][1])
                        active[j][1] = np.append(active[j][1], next_tokens[j])
                        # print("After", active[j][1])
        
        
        if all([val is None for val in active]) and not REQUEST_QUEUE:
            return

def _enqueue(num_entries=20):
    np.random.seed(42)
    for i in range(num_entries):
        prompt: List[int] = np.random.randint(0, high=10, size=100)
        handle = ReturnHandle(i)
        REQUEST_QUEUE.append(Request(prompt, handle))
    
def dequeue():
    if REQUEST_QUEUE:
        return REQUEST_QUEUE.pop(0)
    else:
        return None

if __name__ == "__main__":
    _enqueue(num_entries=20)
    assert len(REQUEST_QUEUE) == 20, "Not initialized correctly"
    process_loop()
    print("\n", "#"*10+"  RESULT  "+"#"*10, "\n")
    for k, v in ReturnHandle.RETURN.items():
        print(f"{k}: {v}")