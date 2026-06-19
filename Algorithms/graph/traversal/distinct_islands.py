from typing import List

def withinBounds(i, j, grid):
    return 0 <= i < len(grid) and 0 <= j < len(grid[i])

def fill(i, j, start_i, start_j, grid, shape, visited):
    if not withinBounds(i, j, grid):
        return
    if grid[i][j] == 0:
        return
    if (i, j) in visited:
        return

    visited.add((i, j))
    # shape from starting point to use as reference point (start x,y)
    # and distinguish between translated islands
    shape.append((i - start_i, j - start_j))

    fill(i + 1, j, start_i, start_j, grid, shape, visited)
    fill(i - 1, j, start_i, start_j, grid, shape, visited)
    fill(i, j + 1, start_i, start_j, grid, shape, visited)
    fill(i, j - 1, start_i, start_j, grid, shape, visited)

def numDistinctIslands(grid: List[List[int]]) -> int:
    visited = set()
    shapes = set()
    # need to search path in order top left to bottom right because anchor
    # starting point is deterministic.
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1 and (i,j) not in visited:
                shape = []
                fill(i, j, i, j, grid, shape, visited)
                # retain traversal path of shape.
                shapes.add(tuple(shape))
    return len(shapes)
