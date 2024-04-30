"""Llama Game
Must make main class
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

# colours
GRAY = (64, 64, 64)
ORANGE = (196, 145, 26)

# fonts
FONT1 = pg.font.SysFont("consolas", 20)

# physics
GRAVITY = 10

# game
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

        self.image = self.SURFS["standing"]
        self.surf = self.image
        self.mask = pg.mask.from_surface(self.image)

        self.front_up = False
        self.jumping = False
        self.crouching = False
        self.walk_cycle_counter = 0

        self.rect = self.surf.get_rect().move(self.offset,
                                              GROUND_HEIGHT - self.height)
        self.v_y = 0
        self.jump_strength = self.height

        self.score = 0
        self.highscore = 0
        self.load_highscore()

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

        self.update_highscore()

    def show_score(self, screen):
        # highscore will glow orange if the player is currently setting it
        highscore_colour = ORANGE if self.highscore == self.score else GRAY
        score_text = FONT1.render(f"{self.score:0>5}", True, GRAY)
        highscore_text = FONT1.render(f"{self.highscore:0>5}",
                                      True, highscore_colour)
        screen.blit(score_text, (self.offset, 20))
        screen.blit(highscore_text, (SCREEN_WIDTH - self.offset - 50, 20))

    def load_highscore(self):
        try:
            highscore_file = open("highscore.txt", "r")
        except IOError:
            highscore_file = open("highscore.txt", "w")
            highscore_file.write("0")
        highscore_file = open("highscore.txt", "r")
        self.highscore = int(highscore_file.read())
        highscore_file.close()

    def save_highscore(self):
        highscore_file = open("highscore.txt", "w")
        highscore_file.write(str(self.highscore))
        highscore_file.close()

    def update_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            self.save_highscore()


class Obstacle(pg.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        # asset is 19x32
        self.width, self.height = 19 * 2, 32 * 2

        self.SURFS = {
            "cacti": pg.transform.scale(pg.image.load(
                "assets/cactus.png"), (self.width, self.height))
        }

        self.image = self.SURFS["cacti"]
        self.surf = self.image
        self.mask = pg.mask.from_surface(self.image)

        self.rect = self.surf.get_rect().move(SCREEN_WIDTH, GROUND_HEIGHT -
                                              self.height)

    def update(self):
        self.rect.x -= 1
        if self.rect.x <= -self.width:
            self.kill()


class Main:
    def __int__(self):
        # initialise display
        pg.display.set_icon(GAME_ICON)
        pg.display.set_caption(GAME_TITLE)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # initialise clock
        self.clock = pg.time.Clock()

        # initialise sprites
        self.ground = Ground(SCREEN_WIDTH, GROUND_HEIGHT, 1)
        self.player = Player()

        # initialise sprite groups
        self.obstacles = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.ground)
        self.all_sprites.add(self.player)

        # initialise obstacle timer
        self.frames_since_obstacle = 0

        # initialise steps per frame variable the cacti will be moving
        self.speed = 16

        # game start
        self.update_screen()
        self.kill_screen(True)

        print("hello")
        running = True
        while running:
            running = self.game_loop()

    def kill_screen(self, start_screen=False):
        if start_screen:
            msg = "Use Space or [▲] to jump, and [▼] to speed down"
        else:
            msg = "You died. Press Space or [▲] to play again."

        text = FONT1.render(msg, True, GRAY)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.screen.blit(text, text_rect)
        pg.display.flip()

        pg.time.wait(1000)
        while True:
            for event in pg.event.get():
                if event.type == KEYDOWN:
                    # stop the loop if user hits Esc key
                    if event.key == K_ESCAPE:
                        return False
                    if event.key == K_UP:
                        return True
                # stop the loop if user hits window close
                elif event.type == QUIT:
                    return False

    # collision detection - moves obstacle by 1 pixel, then checks to
    # see if collision has occurred
    def detect_collision(self):
        steps = int(round(self.speed))
        for step in range(steps):
            self.obstacles.update()  # moves the obstacles
            for obstacle in self.obstacles:
                if pg.sprite.collide_mask(self.player, obstacle):
                    return False
        return True

    def update_screen(self):
        self.screen.fill((255, 255, 255))

        # draw all sprites
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        self.player.show_score(self.screen)

        pg.display.flip()

    def game_loop(self):
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
            if self.frames_since_obstacle % random.randint(11, 32) == 0:
                obstacle = Obstacle()
                self.obstacles.add(obstacle)
                self.all_sprites.add(obstacle)
                self.frames_since_obstacle = 0

            self.player.update(pressed_keys)

            # update obstacles whilst detection collisions
            alive = self.detect_collision()

            # player wins by getting max score (probably impossible)
            if self.player.score == 99999:
                alive = False

            self.update_screen()

            if not alive:
                return self.kill_screen()

            self.clock.tick(FPS)
            self.speed += 0.01
            self.frames_since_obstacle += 1
            self.player.score += 1


main = Main()
print("fsd")

pg.quit()
