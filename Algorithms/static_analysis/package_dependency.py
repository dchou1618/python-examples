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


def find_dependency_cycle_stack(deps: Dict[str, List[str]]) -> List[List[str]]:
    """
    dfs back edges for cycle detection
    """
    visited = set()
    visiting = set()
    # there may be more than one cycle
    path = []
    cycles = []
    for start in deps:
        if start not in visited:
            stack = [(start, False)]
            while stack:
                node, exiting = stack.pop()
                if exiting:
                    path.pop()
                    visiting.remove(node)
                    visited.add(node)
                # back edge
                if node in visiting:
                    idx = path.index(node)
                    cycles.append(path[idx:] + [node])
                    continue
                if node in visited:
                    continue
                visiting.add(node)
                path.append(node)
                stack.append((node, True))
                for neighbor in reversed(deps[node]):
                    stack.append((neighbor, False))
    return cycles
