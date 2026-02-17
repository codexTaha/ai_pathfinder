import pygame as pg  # easier to type

pg.init()

ROWS = 20
COLS = 20
CELL_SIZE = 30
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("AI Pathfinder (phase 1)")

clock = pg.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pg.display.flip()

pg.quit()
