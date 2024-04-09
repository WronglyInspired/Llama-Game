import pygame
import sys

pygame.init()

CLOCK = pygame.time.Clock()  # Essential for regulating the FPS (done under CLOCK.tick() at the bottom)
SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Jumping in PyGame")

X_POSITION, Y_POSITION = 400, 660  # This is the x and y postion of Mario


# 2 surfaces - 1st to represent Mario standing and 2nd comes into play when he's jumping
STANDING_SURFACE = pygame.transform.scale(pygame.image.load(
    "assets/llama_standing.png"), (48, 64))
JUMPING_SURFACE = pygame.transform.scale(pygame.image.load("assets/llama_front_up.png"),
                                         (48, 64))
BACKGROUND = pygame.image.load("assets/cactus.png")  # This is the whole scene
# which makes up Mario's background

mario_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    SCREEN.blit(BACKGROUND, (0, 0))
    SCREEN.blit(JUMPING_SURFACE, mario_rect)

    mario_rect = STANDING_SURFACE.get_rect(center=(X_POSITION, Y_POSITION))
    SCREEN.blit(STANDING_SURFACE, mario_rect)

    pygame.display.update()
    CLOCK.tick(60)  # This is the FPS

