import pygame as pg
from collections import deque

pg.init()

ROWS = 20
COLS = 20
CELL_SIZE = 30
GRID_WIDTH = COLS * CELL_SIZE
SIDE_WIDTH = 200  # panel on the right
WIDTH = GRID_WIDTH + SIDE_WIDTH
HEIGHT = ROWS * CELL_SIZE

EMPTY = 0
WALL = 1
START = 2
END = 3
VISITED = 4
PATH = 5

BLACK = (0, 0, 0)
GRID_LINE = (40, 40, 40)
WALL_COLOR = (80, 80, 80)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
VISITED_COLOR = (0, 0, 255)
PATH_COLOR = (255, 255, 0)

PANEL_BG = (30, 30, 30)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER = (110, 110, 110)
WHITE = (220, 220, 220)
YELLOW = (255, 255, 0)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("AI Pathfinder (phase 1)")

clock = pg.time.Clock()

grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

start_pos = None
end_pos = None

DIRS = [(-1, 0), (0, 1), (1, 0), (1, 1), (0, -1), (-1, -1)]

font = pg.font.SysFont(None, 22)

# simple ui state
current_algorithm = "BFS"
placement_mode = "WALL"  # or "START" or "END"

# buttons as rects (very basic)
algo_bfs_rect = pg.Rect(GRID_WIDTH + 20, 40, 160, 30)
mode_start_rect = pg.Rect(GRID_WIDTH + 20, 100, 160, 30)
mode_end_rect = pg.Rect(GRID_WIDTH + 20, 140, 160, 30)
mode_wall_rect = pg.Rect(GRID_WIDTH + 20, 180, 160, 30)
run_rect = pg.Rect(GRID_WIDTH + 20, 240, 160, 40)
clear_rect = pg.Rect(GRID_WIDTH + 20, 300, 160, 30)

def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE
            y = r * CELL_SIZE

            val = grid[r][c]
            color = BLACK
            if val == WALL:
                color = WALL_COLOR
            elif val == START:
                color = START_COLOR
            elif val == END:
                color = END_COLOR
            elif val == VISITED:
                color = VISITED_COLOR
            elif val == PATH:
                color = PATH_COLOR

            rect = pg.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(screen, color, rect)
            pg.draw.rect(screen, GRID_LINE, rect, 1)

def draw_button(rect, text, selected=False):
    mouse_pos = pg.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        color = BUTTON_HOVER
    else:
        color = BUTTON_COLOR
    if selected:
        color = (color[0], color[1], min(color[2] + 60, 255))

    pg.draw.rect(screen, color, rect, border_radius=4)
    pg.draw.rect(screen, WHITE, rect, 1, border_radius=4)

    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_panel():
    # background
    panel_rect = pg.Rect(GRID_WIDTH, 0, SIDE_WIDTH, HEIGHT)
    pg.draw.rect(screen, PANEL_BG, panel_rect)

    title = font.render("Controls", True, YELLOW)
    screen.blit(title, (GRID_WIDTH + 20, 10))

    # algorithm section
    algo_label = font.render("Algorithm:", True, WHITE)
    screen.blit(algo_label, (GRID_WIDTH + 20, 25))
    draw_button(algo_bfs_rect, "BFS (only for now)", current_algorithm == "BFS")

    # placement section
    place_label = font.render("Placement mode:", True, WHITE)
    screen.blit(place_label, (GRID_WIDTH + 20, 80))
    draw_button(mode_start_rect, "Place START", placement_mode == "START")
    draw_button(mode_end_rect, "Place END", placement_mode == "END")
    draw_button(mode_wall_rect, "Place WALLS", placement_mode == "WALL")

    # run + clear
    draw_button(run_rect, "Run search", False)
    draw_button(clear_rect, "Clear grid", False)

def handle_grid_click(event):
    global start_pos, end_pos

    x, y = event.pos
    if x >= GRID_WIDTH:
        return  # click was on panel, not grid

    c = x // CELL_SIZE
    r = y // CELL_SIZE

    if r < 0 or r >= ROWS or c < 0 or c >= COLS:
        return

    if placement_mode == "WALL":
        if grid[r][c] == EMPTY:
            grid[r][c] = WALL
        elif grid[r][c] == WALL:
            grid[r][c] = EMPTY
    elif placement_mode == "START":
        # clear old start
        if start_pos is not None:
            sr, sc = start_pos
            if grid[sr][sc] == START:
                grid[sr][sc] = EMPTY
        start_pos = (r, c)
        grid[r][c] = START
    elif placement_mode == "END":
        if end_pos is not None:
            er, ec = end_pos
            if grid[er][ec] == END:
                grid[er][ec] = EMPTY
        end_pos = (r, c)
        grid[r][c] = END

def handle_panel_click(event):
    global placement_mode, current_algorithm

    if algo_bfs_rect.collidepoint(event.pos):
        current_algorithm = "BFS"

    elif mode_start_rect.collidepoint(event.pos):
        placement_mode = "START"
    elif mode_end_rect.collidepoint(event.pos):
        placement_mode = "END"
    elif mode_wall_rect.collidepoint(event.pos):
        placement_mode = "WALL"
    elif run_rect.collidepoint(event.pos):
        if current_algorithm == "BFS":
            bfs()
    elif clear_rect.collidepoint(event.pos):
        clear_grid()

def clear_grid():
    global start_pos, end_pos
    for r in range(ROWS):
        for c in range(COLS):
            grid[r][c] = EMPTY
    start_pos = None
    end_pos = None

def reset_search_only():
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == VISITED or grid[r][c] == PATH:
                grid[r][c] = EMPTY

def get_neighbors(r, c):
    res = []
    for dr, dc in DIRS:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if grid[nr][nc] != WALL:
                res.append((nr, nc))
    return res

def bfs():
    if start_pos is None or end_pos is None:
        print("need start and end first")
        return

    reset_search_only()

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

        for nr, nc in get_neighbors(r, c):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = (r, c)
                q.append((nr, nc))

        redraw_window()
        pg.time.wait(20)

    if found:
        cur = end_pos
        while cur != start_pos:
            r, c = cur
            if cur != end_pos:
                grid[r][c] = PATH
            cur = parent.get(cur)
            if cur is None:
                break
            redraw_window()
            pg.time.wait(20)
        print("bfs done")
    else:
        print("no path found :(")

def redraw_window():
    screen.fill(BLACK)
    draw_grid()
    draw_panel()
    pg.display.flip()

def main_loop():
    running = True
    while running:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.pos[0] < GRID_WIDTH:
                    handle_grid_click(event)
                else:
                    handle_panel_click(event)

        redraw_window()

    pg.quit()

if __name__ == "__main__":
    main_loop()
