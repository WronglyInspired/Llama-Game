import pygame as pg
from pygame.locals import (
    K_SPACE,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
pg.init()

# create constants
GAME_ICON = pg.image.load("assets/game_icon.png")
GAME_TITLE = "Lluis the Llama"

GRAY = (64, 64, 64)

FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 480


# initialise display
pg.display.set_icon(GAME_ICON)
pg.display.set_caption(GAME_TITLE)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pg.time.Clock()

# game loop
running = True
while running:
    for event in pg.event.get():
        if event.type == KEYDOWN:
            # stop the loop if user hits Esc key
            if event.key == K_ESCAPE:
                running = False
        # stop the loop if user hits window close
        elif event.type == QUIT:
            running = False

    screen.fill((255, 255, 255))
    pg.display.flip()

    clock.tick(FPS)

pg.quit()
