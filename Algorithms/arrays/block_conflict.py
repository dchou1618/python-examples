"""
block_conflict.py
Module assumes two operations
[1,x] lays an obstacle at position x
[2,x,size] lays a block of size-1 centered around position x
Input: list of operations
Output: binary string of 0s and 1s, where 1 indicates that
operation 2 was successful and 0 indicates that operation 2 failed 
due to a conflict with a previous operation

Naive method uses O(q*n) worse case
Sorted set uses O(q*log(n)) worse case
"""
from typing import List
from sortedcontainers import SortedSet

def block_conflict(operations: List[List[int]]) -> str:
    """
    block_conflict function takes a list of operations and 
    returns a binary string indicating the success or 
    failure of each operation 2.
    """
    res = []
    obstacles = SortedSet()
    for op in operations:
        x = op[1]
        if op[0] == 1:
            obstacles.add(x)
        else:
            if op[0] != 2:
                raise ValueError("Invalid operation type")
            size = op[2]
            left = x - (size - 1) // 2
            right = x + (size - 1) // 2
            idx = obstacles.bisect_left(left)
            res.append("1" if idx == len(obstacles) or obstacles[idx] > right else "0")
    return "".join(res)

