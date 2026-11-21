import pygame
from ball import Ball

pygame.init()

# Screen
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode(
    (screen_width, screen_height)
)

pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

# Create ball in the center
ball = Ball(
    screen_width // 2,
    screen_height // 2
)

running = True

while running:

    screen.fill((255, 255, 255))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                ball.move("up", screen_width, screen_height)

            elif event.key == pygame.K_DOWN:
                ball.move("down", screen_width, screen_height)

            elif event.key == pygame.K_LEFT:
                ball.move("left", screen_width, screen_height)

            elif event.key == pygame.K_RIGHT:
                ball.move("right", screen_width, screen_height)

    # Draw ball
    ball.draw(screen)

    pygame.display.flip()

    # FPS
    clock.tick(60)

pygame.quit()