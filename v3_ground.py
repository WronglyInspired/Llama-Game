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
DOT_SIZE = 4  # the size a pixel in the art will be expanded to

FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 320 * DOT_SIZE, 120 * DOT_SIZE
GROUND_HEIGHT = SCREEN_HEIGHT - 20 * DOT_SIZE


class Ground(pg.sprite.Sprite):
    def __init__(self, width, height, thickness):
        super(Ground, self).__init__()
        self.width = width
        self.height = height
        self.thickness = thickness * DOT_SIZE

        self.surf = pg.Surface((self.width, self.thickness))
        self.surf.fill(GRAY)
        self.rect = self.surf.get_rect().move(0, height)


# initialise display
pg.display.set_icon(GAME_ICON)
pg.display.set_caption(GAME_TITLE)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# initialise clock
clock = pg.time.Clock()

# initialise sprites
ground = Ground(SCREEN_WIDTH, GROUND_HEIGHT, 1)

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
    screen.blit(ground.surf, ground.rect)
    pg.display.flip()

    clock.tick(FPS)

pg.quit()
