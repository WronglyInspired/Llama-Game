"""Llama Game
"""
import pygame as pg
from pygame.locals import (
    K_SPACE,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import random

pg.init()

# create constants
GAME_ICON = pg.image.load("assets/game_icon.png")
GAME_TITLE = "Lluis the Llama"

GRAY = (64, 64, 64)

GRAVITY = 10

FPS = 30
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 480
GROUND_HEIGHT = SCREEN_HEIGHT - 80


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

        self.SURFS = {
            "standing": pg.transform.scale(pg.image.load(
                "assets/llama_standing.png"), (self.width, self.height)),
            "front_up": pg.transform.scale(pg.image.load(
                "assets/llama_front_up.png"), (self.width, self.height)),
            "back_up": pg.transform.scale(pg.image.load(
                "assets/llama_back_up.png"), (self.width, self.height)),
            "crouching": pg.transform.scale(pg.image.load(
                "assets/llama_ducking.png"), (self.width, self.height))
        }

        self.surf = self.SURFS["standing"]
        self.front_up = False
        self.jumping = False
        self.crouching = False
        self.walk_cycle_counter = 0

        self.rect = self.surf.get_rect().move(self.offset,
                                              GROUND_HEIGHT - self.height)
        self.v_y = 0
        self.jump_strength = self.height

    def update(self, pressed_keys):
        if ((pressed_keys[K_UP] or pressed_keys[K_SPACE]) and
                self.rect.y >= GROUND_HEIGHT - self.height):
            self.v_y = self.jump_strength
            self.jumping = True

        elif pressed_keys[K_DOWN]:
            self.v_y = - self.jump_strength
            self.jumping, self.crouching = False, True

        self.rect.y -= self.v_y
        self.v_y -= GRAVITY

        # stop from going through ground
        if self.rect.y >= GROUND_HEIGHT - self.height:
            self.rect.y = GROUND_HEIGHT - self.height
            self.v_y = 0
            self.jumping, self.crouching = False, False

        # llama animation
        if self.jumping:
            self.surf = self.SURFS["standing"]
        if self.crouching:
            self.surf = self.SURFS["crouching"]
        else:
            if self.front_up:
                self.surf = self.SURFS["front_up"]
            else:
                self.surf = self.SURFS["back_up"]

        # toggle front_up variable
        if self.walk_cycle_counter == 4:
            self.walk_cycle_counter = 0
            self.front_up = not self.front_up
        self.walk_cycle_counter += 1


class Obstacle(pg.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        # asset is 19x32
        self.width, self.height = 19 * 2, 32 * 2

        self.SURFS = {
            "cacti": pg.transform.scale(pg.image.load(
                "assets/cactus.png"), (self.width, self.height))
        }

        self.surf = self.SURFS["cacti"]

        self.rect = self.surf.get_rect().move(SCREEN_WIDTH, GROUND_HEIGHT -
                                              self.height)

    def update(self, step):
        self.rect.x -= step
        if self.rect.x <= -self.width:
            self.kill()


def kill_screen():
    while True:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                # stop the loop if user hits Esc key
                if event.key == K_ESCAPE:
                    return False
                if event.key == K_SPACE:
                    return True
            # stop the loop if user hits window close
            elif event.type == QUIT:
                return False
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
    obstacles = pg.sprite.Group()
    all_sprites = pg.sprite.Group()
    all_sprites.add(ground)
    all_sprites.add(player)

    # initialise obstacle timer
    frames_since_obstacle = 0

    # initialise step / speed variable
    speed = 16

    # game loop
    while True:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                # stop the loop if user hits Esc key
                if event.key == K_ESCAPE:
                    return False
            # stop the loop if user hits window close
            elif event.type == QUIT:
                return False

        pressed_keys = pg.key.get_pressed()

        # add obstacles
        if frames_since_obstacle % random.randint(16, 32) == 0:
            obstacle = Obstacle()
            obstacles.add(obstacle)
            all_sprites.add(obstacle)
            frames_since_obstacle = 0

        player.update(pressed_keys)

        obstacles.update(speed)

        screen.fill((255, 255, 255))

        # draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        pg.display.flip()

        # check if obstacles have collided with the player
        if pg.sprite.spritecollideany(player, obstacles):
            return kill_screen()

        clock.tick(FPS)
        frames_since_obstacle += 1


running = True
while running:
    running = main()

pg.quit()
