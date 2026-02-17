from collections import deque
import heapq

EMPTY = 0
WALL = 1
START = 2
END = 3
VISITED = 4
PATH = 5

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
            new_cost = cost + 1
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

# ----- Depth-Limited Search (DLS) and IDDFS -----

def dls(grid, start_pos, end_pos, limit, step_callback=None):
    if start_pos is None or end_pos is None:
        print("need start and end first")
        return False

    reset_search_only(grid)

    stack = [(start_pos, 0)]
    parent = {}
    visited = set([start_pos])
    found = False

    while stack:
        (r, c), depth = stack.pop()

        if (r, c) != start_pos and (r, c) != end_pos:
            grid[r][c] = VISITED

        if (r, c) == end_pos:
            found = True
            break

        if depth < limit:
            for nr, nc in reversed(get_neighbors(grid, r, c)):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    stack.append(((nr, nc), depth + 1))

        if step_callback:
            step_callback()

    if found:
        _reconstruct_path(grid, parent, start_pos, end_pos, step_callback)
        print("dls done (limit =", limit, ")")
        return True
    else:
        print("dls: not found up to limit", limit)
        return False

def iddfs(grid, start_pos, end_pos, max_limit, step_callback=None):
    if start_pos is None or end_pos is None:
        print("need start and end first")
        return False

    for limit in range(max_limit + 1):
        print("iddfs: trying limit", limit)
        # run dls; it already calls reset_search_only
        if dls(grid, start_pos, end_pos, limit, step_callback):
            print("iddfs found at depth", limit)
            return True
    print("iddfs: not found up to max_limit", max_limit)
    return False

# ----- Bidirectional BFS -----

def bidirectional_bfs(grid, start_pos, end_pos, step_callback=None):
    if start_pos is None or end_pos is None:
        print("need start and end first")
        return False

    reset_search_only(grid)

    q_start = deque([start_pos])
    q_end = deque([end_pos])
    parent_start = {start_pos: None}
    parent_end = {end_pos: None}
    visited_start = {start_pos}
    visited_end = {end_pos}
    meeting_node = None

    while q_start and q_end:
        # expand from start side
        rs, cs = q_start.popleft()
        if (rs, cs) != start_pos and (rs, cs) != end_pos:
            grid[rs][cs] = VISITED

        for nr, nc in get_neighbors(grid, rs, cs):
            if (nr, nc) not in visited_start and (nr, nc) != end_pos:
                visited_start.add((nr, nc))
                parent_start[(nr, nc)] = (rs, cs)
                q_start.append((nr, nc))
                if (nr, nc) in visited_end:
                    meeting_node = (nr, nc)
                    break
        if step_callback:
            step_callback()
        if meeting_node:
            break

        # expand from end side
        re, ce = q_end.popleft()
        if (re, ce) != start_pos and (re, ce) != end_pos:
            grid[re][ce] = VISITED

        for nr, nc in get_neighbors(grid, re, ce):
            if (nr, nc) not in visited_end and (nr, nc) != start_pos:
                visited_end.add((nr, nc))
                parent_end[(nr, nc)] = (re, ce)
                q_end.append((nr, nc))
                if (nr, nc) in visited_start:
                    meeting_node = (nr, nc)
                    break
        if step_callback:
            step_callback()
        if meeting_node:
            break

    if not meeting_node:
        print("bidirectional: no path")
        return False

    # reconstruct path from start -> meeting
    path_nodes = []
    cur = meeting_node
    while cur is not None:
        path_nodes.append(cur)
        cur = parent_start.get(cur)
    path_nodes.reverse()  # from start to meeting

    # then meeting -> end
    cur = meeting_node
    cur = parent_end.get(cur)
    while cur is not None:
        path_nodes.append(cur)
        cur = parent_end.get(cur)

    for idx, (r, c) in enumerate(path_nodes):
        if (r, c) != start_pos and (r, c) != end_pos:
            grid[r][c] = PATH
        if step_callback:
            step_callback()

    print("bidirectional bfs done")
    return True
