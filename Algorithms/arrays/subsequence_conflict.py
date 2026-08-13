from typing import List

def dfs(start, adj_lst, visited, seen):
    """
    return: if cycle is detected
    """
    if start in seen:
        return True
    if start in visited or start not in adj_lst:
        return False 
    seen.add(start)
    for neighbor in adj_lst[start]:
        if dfs(neighbor, adj_lst, visited, seen):
            return True
    seen.remove(start)
    visited.add(start)
    return False

def subsequence(input_lsts: List[List[int]]):
    """
    input_lsts list of lists
    """
    adj_lst = dict()

    for l in input_lsts:
        for i in range(1, len(l)):
            adj_lst.setdefault(l[i-1], []).append(l[i])

    visited = set()
    for node in adj_lst.keys():
        if node not in visited:
            is_cycle = dfs(node, adj_lst, visited, set())
            if is_cycle:
                return False
    return True
