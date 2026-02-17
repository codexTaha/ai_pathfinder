from collections import deque
import heapq

# cell types (must match main.py)
EMPTY = 0
WALL = 1
START = 2
END = 3
VISITED = 4
PATH = 5

# directions: up, right, down, down-right, left, up-left
DIRS = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]

def reset_search_only(grid):
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == VISITED or grid[r][c] == PATH:
                grid[r][c] = EMPTY

def get_neighbors(grid, r, c):
    rows = len(grid)
    cols = len(grid[0])
    result = []
    for dr, dc in DIRS:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] != WALL:
                result.append((nr, nc))
    return result

def _reconstruct_path(grid, parent, start_pos, end_pos, step_callback):
    cur = end_pos
    while cur != start_pos:
        r, c = cur
        if cur != end_pos:
            grid[r][c] = PATH
        cur = parent.get(cur)
        if cur is None:
            break
        if step_callback:
            step_callback()
    return

def bfs(grid, start_pos, end_pos, step_callback=None):
    if start_pos is None or end_pos is None:
        print("need start and end first")
        return False

    reset_search_only(grid)

    q = deque()
    q.append(start_pos)
    visited = set([start_pos])
    parent = {}
    found = False

    while q:
        r, c = q.popleft()

        if (r, c) != start_pos and (r, c) != end_pos:
            grid[r][c] = VISITED

        if (r, c) == end_pos:
            found = True
            break

        for nr, nc in get_neighbors(grid, r, c):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                q.append((nr, nc))

        if step_callback:
            step_callback()

    if found:
        _reconstruct_path(grid, parent, start_pos, end_pos, step_callback)
        print("bfs done")
        return True
    else:
        print("no path found :(")
        return False

def dfs(grid, start_pos, end_pos, step_callback=None):
    if start_pos is None or end_pos is None:
        print("need start and end first")
        return False

    reset_search_only(grid)

    stack = [start_pos]
    visited = set([start_pos])
    parent = {}
    found = False

    while stack:
        r, c = stack.pop()

        if (r, c) != start_pos and (r, c) != end_pos:
            grid[r][c] = VISITED

        if (r, c) == end_pos:
            found = True
            break

        for nr, nc in reversed(get_neighbors(grid, r, c)):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                stack.append((nr, nc))

        if step_callback:
            step_callback()

    if found:
        _reconstruct_path(grid, parent, start_pos, end_pos, step_callback)
        print("dfs done")
        return True
    else:
        print("no path found :(")
        return False

def ucs(grid, start_pos, end_pos, step_callback=None):
    if start_pos is None or end_pos is None:
        print("need start and end first")
        return False

    reset_search_only(grid)

    pq = []
    heapq.heappush(pq, (0, start_pos))
    parent = {}
    cost_so_far = {start_pos: 0}
    found = False

    while pq:
        cost, (r, c) = heapq.heappop(pq)

        if (r, c) != start_pos and (r, c) != end_pos:
            grid[r][c] = VISITED

        if (r, c) == end_pos:
            found = True
            break

        for nr, nc in get_neighbors(grid, r, c):
            new_cost = cost + 1  # all edges cost 1 here [web:20][web:102]
            if (nr, nc) not in cost_so_far or new_cost < cost_so_far[(nr, nc)]:
                cost_so_far[(nr, nc)] = new_cost
                parent[(nr, nc)] = (r, c)
                heapq.heappush(pq, (new_cost, (nr, nc)))

        if step_callback:
            step_callback()

    if found:
        _reconstruct_path(grid, parent, start_pos, end_pos, step_callback)
        print("ucs done")
        return True
    else:
        print("no path found :(")
        return False
