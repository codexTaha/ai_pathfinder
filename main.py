import pygame as pg
from collections import deque  # will use later

pg.init()

ROWS = 20
COLS = 20
CELL_SIZE = 30
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# cell values
EMPTY = 0
WALL = 1
START = 2
END = 3
VISITED = 4
PATH = 5

# colors
BLACK = (0, 0, 0)
GRID_LINE = (40, 40, 40)
WALL_COLOR = (80, 80, 80)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
VISITED_COLOR = (0, 0, 255)
PATH_COLOR = (255, 255, 0)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("AI Pathfinder (phase 1)")

clock = pg.time.Clock()

# grid is just ints, nothing fancy
grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

start_pos = None
end_pos = None

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

def handle_mouse(event):
    global start_pos, end_pos

    x, y = pg.mouse.get_pos()
    c = x // CELL_SIZE
    r = y // CELL_SIZE

    if r < 0 or r >= ROWS or c < 0 or c >= COLS:
        return

    if event.button == 1:  # left -> wall toggle
        if grid[r][c] == EMPTY:
            grid[r][c] = WALL
        elif grid[r][c] == WALL:
            grid[r][c] = EMPTY

    elif event.button == 3:  # right -> start then end
        if start_pos is None:
            start_pos = (r, c)
            grid[r][c] = START
        elif end_pos is None and (r, c) != start_pos:
            end_pos = (r, c)
            grid[r][c] = END

def redraw_window():
    screen.fill(BLACK)
    draw_grid()
    pg.display.flip()

running = True

while running:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            handle_mouse(event)

    redraw_window()

pg.quit()
