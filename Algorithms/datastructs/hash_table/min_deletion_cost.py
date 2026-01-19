from collections import defaultdict
from typing import List

def minCost(s: str, cost: List[int]) -> int:
    t = defaultdict(int)
    max_cost, sum_cost = 0, 0
    for i in range(len(s)):
        t[s[i]] += cost[i]
        max_cost = max(max_cost, t[s[i]])
        sum_cost += cost[i]
    if len(t) > 1:
        return sum_cost - max_cost
    else:
        return 0
    
def minCost2(s: str, cost: List[int]) -> int:
    arr = [0]*26
    max_cost, sum_cost = 0, 0
    for i in range(len(s)):
        idx = ord(s[i]) - ord('a')
        arr[idx] += cost[i]
        max_cost = max(max_cost, arr[idx])
        sum_cost += cost[i]
    return sum_cost - max_cost
