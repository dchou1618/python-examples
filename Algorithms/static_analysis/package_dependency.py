from typing import Dict, List

def find_dependency_cycle(deps: Dict[str, List[str]]) -> List[List[str]]:
    """
    dfs back edges for cycle detection
    """
    visited = set()
    visiting = set()
    # there may be more than one cycle
    path = []
    cycles = []
    def dfs(node):
        if node in visiting:
            idx = path.index(node)
            cycles.append(path[idx:] + [node])
            return

        if node in visited:
            return

        visiting.add(node)
        visited.add(node)
        path.append(node)

        for neighbor in deps[node]:
            dfs(neighbor)
        
        path.pop()
        visiting.remove(node)


    for node in deps:
        if node not in visited:
            dfs(node)

    return cycles