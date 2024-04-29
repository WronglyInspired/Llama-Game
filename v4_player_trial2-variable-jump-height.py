"""Llama Game
+ Player jump ability -- variable jump height"""
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

GRAVITY = 10

FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 480
GROUND_HEIGHT = SCREEN_HEIGHT - 80


class Velocity:
    def __init__(self):
        self.x = 0
        self.y = 0


class Ground(pg.sprite.Sprite):
    def __init__(self, width, height, thickness):
        super(Ground, self).__init__()
        self.width = width
        self.height = height
        self.thickness = thickness * 4

        self.surf = pg.Surface((self.width, self.thickness))
        self.surf.fill(GRAY)
        self.rect = self.surf.get_rect().move(0, height)


class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # asset is 22x32
        self.width, self.height = 22 * 2, 32 * 2
        self.offset = 40

        self.surf = pg.Surface((self.width, self.height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect().move(self.offset,
                                              GROUND_HEIGHT - self.height)
        self.v_y = 0

    def update(self, pressed_keys, key_up):
        jump_strength = self.height

        if ((pressed_keys[K_UP] or pressed_keys[K_SPACE]) and
                self.rect.y >= GROUND_HEIGHT - self.height):
            self.v_y = jump_strength

        elif key_up:
            self.v_y = jump_strength

        self.rect.y -= self.v_y
        self.v_y -= GRAVITY

        # stop from going through ground
        if self.rect.y >= GROUND_HEIGHT - self.height:
            self.rect.y = GROUND_HEIGHT - self.height
            self.v_y = 0


def main():
    # initialise display
    pg.display.set_icon(GAME_ICON)
    pg.display.set_caption(GAME_TITLE)
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # initialise clock
    clock = pg.time.Clock()

    # initialise sprites
    ground = Ground(SCREEN_WIDTH, GROUND_HEIGHT, 1)
    player = Player()

    # initialise sprite groups
    all_sprites = pg.sprite.Group()
    all_sprites.add(ground)
    all_sprites.add(player)

    # game loop
    while True:
        key_up = False
        for event in pg.event.get():
            if event.type == KEYDOWN:
                # stop the loop if user hits Esc key
                if event.key == K_ESCAPE:
                    return

                key = pg.key.name(event.key)
                print(key, "Key is pressed")
            if event.type == pg.KEYUP:
                key = pg.key.name(event.key)
                print(key, "Key is released")
                key_up = True

            # stop the loop if user hits window close
            elif event.type == QUIT:
                return

        pressed_keys = pg.key.get_pressed()

        player.update(pressed_keys, key_up)

        screen.fill((255, 255, 255))
        screen.blit(ground.surf, ground.rect)
        screen.blit(player.surf, player.rect)
        pg.display.flip()

        clock.tick(FPS)
        print(pg.time.get_ticks())


if __name__ == "__main__":
    main()
    pg.quit()
