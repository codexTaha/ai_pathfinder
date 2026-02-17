import pygame as pg

pg.init()

ROWS = 20
COLS = 20
CELL_SIZE = 30
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

BLACK = (0, 0, 0)
GRID_LINE = (40, 40, 40)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("AI Pathfinder (phase 1)")

clock = pg.time.Clock()

def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            rect = pg.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(screen, GRID_LINE, rect, 1)  # only border

running = True

while running:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(BLACK)
    draw_grid()
    pg.display.flip()

pg.quit()
