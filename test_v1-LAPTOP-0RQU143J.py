import pygame as pg
import pygame.display
import random
from pygame.locals import (
    K_SPACE,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 480
GROUND_HEIGHT = SCREEN_HEIGHT - 80
print(GROUND_HEIGHT)
BLOCK_SIZE = 5
GRAVITY = 7
FPS = 30
PLAYER_OFFSET = 50

pg.init()


class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # must be multiple of 22x32
        self.width, self.height = 22 * 2, 32 * 2

        self.SURFS = {
            "standing": pg.transform.scale(pg.image.load(
                "assets/llama_standing.png"), (self.width, self.height)),
            "front_up": pg.transform.scale(pg.image.load(
                "assets/llama_front_up.png"), (self.width, self.height)),
            "back_up": pg.transform.scale(pg.image.load(
                "assets/llama_back_up.png"), (self.width, self.height))
        }

        self.surf = self.SURFS["standing"]
        self.front_up = False
        self.jumping = False
        self.walk_cycle_delay = 0

        self.rect = self.surf.get_rect().move(PLAYER_OFFSET, GROUND_HEIGHT -
                                              self.height)

        self.v = 0  # y-velocity

    def update(self, pressed_keys):
        if pressed_keys[K_UP] or pressed_keys[K_SPACE]:
            if self.rect.y >= GROUND_HEIGHT - self.height:
                self.v = 50  # negative is up
                self.jumping = True

        # move rect according to velocity
        self.rect.y -= self.v

        # gravity accelerates v
        self.v -= GRAVITY

        # stop from going through ground
        if self.rect.y >= GROUND_HEIGHT - self.height:
            self.rect.y = GROUND_HEIGHT - self.height
            self.v = 0
            self.jumping = False

        # llama animation
        if self.jumping:
            self.surf = self.SURFS["standing"]
        else:
            if self.front_up:
                self.surf = self.SURFS["front_up"]
            else:
                self.surf = self.SURFS["back_up"]

        # toggle front_up variable
        if self.walk_cycle_delay == 4:
            self.walk_cycle_delay = 0
            self.front_up = not self.front_up

        self.walk_cycle_delay += 1

        # print(f"y: {self.rect.y} | v: {round(self.v)}")


class Obstacle(pg.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()

        self.width, self.height = 22 * 2, 32 * 2

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
            del self


class Cactus(Obstacle):
    pass


class Ground:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = GROUND_HEIGHT
        self.thickness = BLOCK_SIZE

        self.surf = pygame.Surface((self.width, self.thickness))
        self.surf.fill((64, 64, 64))


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# instantiate player
player = Player()
ground = Ground()
speed = 16
obstacles = [Obstacle()]
frames_since_obstacle = 0

clock = pg.time.Clock()

running = True

# Main game loop
while running:
    for event in pg.event.get():
        if event.type == KEYDOWN:
            # stop the loop if user hits Esc key
            if event.key == K_ESCAPE:
                running = False

        # stop the loop if user hits window close
        elif event.type == QUIT:
            running = False

    # get the set of keys pressed at the start of that frame
    pressed_keys = pg.key.get_pressed()

    if frames_since_obstacle % random.randint(16, 32) == 0:
        obstacles.append(Obstacle())
        frames_since_obstacle = 0

    player.update(pressed_keys)

    screen.fill((255, 255, 255))

    screen.blit(ground.surf, (0, ground.height))
    for i in obstacles:
        i.update(speed)
        screen.blit(i.surf, i.rect)

    screen.blit(player.surf, player.rect)

    pg.display.flip()

    clock.tick(FPS)
    speed += 0.01
    frames_since_obstacle += 1
