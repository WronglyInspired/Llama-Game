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

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 480

# initialise display
pg.display.set_icon(GAME_ICON)
pg.display.set_caption(GAME_TITLE)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# test that it works
import time
time.sleep(5)
pg.quit()
