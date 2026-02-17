import pygame as pg

from algorithms.search_algos import (
    bfs, dfs, ucs,
    dls, iddfs, bidirectional_bfs,
    EMPTY, WALL, START, END, VISITED, PATH
)

pg.init()

ROWS = 20
COLS = 20
CELL_SIZE = 30
GRID_WIDTH = COLS * CELL_SIZE
SIDE_WIDTH = 230
WIDTH = GRID_WIDTH + SIDE_WIDTH
HEIGHT = ROWS * CELL_SIZE

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
pg.display.set_caption("AI Pathfinder")

clock = pg.time.Clock()

grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

start_pos = None
end_pos = None

font = pg.font.SysFont(None, 22)

current_algorithm = "BFS"
placement_mode = "WALL"

algo_bfs_rect  = pg.Rect(GRID_WIDTH + 20, 40, 190, 28)
algo_dfs_rect  = pg.Rect(GRID_WIDTH + 20, 72, 190, 28)
algo_ucs_rect  = pg.Rect(GRID_WIDTH + 20, 104, 190, 28)
algo_dls_rect  = pg.Rect(GRID_WIDTH + 20, 136, 190, 28)
algo_iddfs_rect = pg.Rect(GRID_WIDTH + 20, 168, 190, 28)
algo_bi_rect   = pg.Rect(GRID_WIDTH + 20, 200, 190, 28)

mode_start_rect = pg.Rect(GRID_WIDTH + 20, 250, 190, 28)
mode_end_rect   = pg.Rect(GRID_WIDTH + 20, 282, 190, 28)
mode_wall_rect  = pg.Rect(GRID_WIDTH + 20, 314, 190, 28)

run_rect   = pg.Rect(GRID_WIDTH + 20, 360, 190, 40)
clear_rect = pg.Rect(GRID_WIDTH + 20, 408, 190, 28)

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
        color = (min(color[0]+30,255), min(color[1]+30,255), color[2])

    pg.draw.rect(screen, color, rect, border_radius=4)
    pg.draw.rect(screen, WHITE, rect, 1, border_radius=4)

    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_panel():
    panel_rect = pg.Rect(GRID_WIDTH, 0, SIDE_WIDTH, HEIGHT)
    pg.draw.rect(screen, PANEL_BG, panel_rect)

    title = font.render("Algorithms:", True, YELLOW)
    screen.blit(title, (GRID_WIDTH + 20, 12))

    draw_button(algo_bfs_rect,  "1) BFS",  current_algorithm == "BFS")
    draw_button(algo_dfs_rect,  "2) DFS",  current_algorithm == "DFS")
    draw_button(algo_ucs_rect,  "3) UCS",  current_algorithm == "UCS")
    draw_button(algo_dls_rect,  "4) DLS",  current_algorithm == "DLS")
    draw_button(algo_iddfs_rect,"5) IDDFS",current_algorithm == "IDDFS")
    draw_button(algo_bi_rect,   "6) Bidirectional", current_algorithm == "BIDIR")

    place_label = font.render("Placement:", True, YELLOW)
    screen.blit(place_label, (GRID_WIDTH + 20, 230))

    draw_button(mode_start_rect, "Place START", placement_mode == "START")
    draw_button(mode_end_rect,   "Place END",   placement_mode == "END")
    draw_button(mode_wall_rect,  "Place WALLS", placement_mode == "WALL")

    draw_button(run_rect, "Run " + current_algorithm, False)
    draw_button(clear_rect, "Clear grid", False)

def handle_grid_click(event):
    global start_pos, end_pos

    x, y = event.pos
    if x >= GRID_WIDTH:
        return
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
    elif algo_dfs_rect.collidepoint(event.pos):
        current_algorithm = "DFS"
    elif algo_ucs_rect.collidepoint(event.pos):
        current_algorithm = "UCS"
    elif algo_dls_rect.collidepoint(event.pos):
        current_algorithm = "DLS"
    elif algo_iddfs_rect.collidepoint(event.pos):
        current_algorithm = "IDDFS"
    elif algo_bi_rect.collidepoint(event.pos):
        current_algorithm = "BIDIR"

    elif mode_start_rect.collidepoint(event.pos):
        placement_mode = "START"
    elif mode_end_rect.collidepoint(event.pos):
        placement_mode = "END"
    elif mode_wall_rect.collidepoint(event.pos):
        placement_mode = "WALL"

    elif run_rect.collidepoint(event.pos):
        run_current_algorithm()
    elif clear_rect.collidepoint(event.pos):
        clear_grid()

def clear_grid():
    global start_pos, end_pos
    for r in range(ROWS):
        for c in range(COLS):
            grid[r][c] = EMPTY
    start_pos = None
    end_pos = None

def step_callback():
    redraw_window()
    pg.time.wait(20)

def run_current_algorithm():
    if current_algorithm == "BFS":
        bfs(grid, start_pos, end_pos, step_callback)
    elif current_algorithm == "DFS":
        dfs(grid, start_pos, end_pos, step_callback)
    elif current_algorithm == "UCS":
        ucs(grid, start_pos, end_pos, step_callback)
    elif current_algorithm == "DLS":
        # choose a reasonable limit; grid max depth is ROWS*COLS
        dls(grid, start_pos, end_pos, limit=40, step_callback=step_callback)
    elif current_algorithm == "IDDFS":
        iddfs(grid, start_pos, end_pos, max_limit=40, step_callback=step_callback)
    elif current_algorithm == "BIDIR":
        bidirectional_bfs(grid, start_pos, end_pos, step_callback)

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
