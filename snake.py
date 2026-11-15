
import pygame
import random

pygame.init()

size = (900, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
grid_size = 30

# Colors
BACKGROUND = (25, 25, 35)
GRID_COLOR = (35, 35, 50)
SNAKE_COLOR = (0, 200, 100)
HEAD_COLOR = (100, 255, 150)
FOOD_COLOR = (255, 70, 70)
TEXT_COLOR = (255, 255, 255)

score = 0
score_font = pygame.font.Font(None, 30)

snake = [[90, 360], [90, 390], [90, 420]]
direction = [0, -grid_size]

food_pos = []
food_eaten = True


# Background
def draw_background():
    screen.fill(BACKGROUND)

    for x in range(0, size[0], grid_size):
        for y in range(0, size[1], grid_size):
            if (x // grid_size + y // grid_size) % 2 == 0:
                pygame.draw.rect(
                    screen, GRID_COLOR,
                    (x, y, grid_size, grid_size)
                )


# Draw snake
def draw_snake():
    for i, segment in enumerate(snake):
        color = HEAD_COLOR if i == 0 else SNAKE_COLOR

        pygame.draw.rect(
            screen,
            color,
            (segment[0], segment[1],
             grid_size - 2, grid_size - 2),
            border_radius=7
        )


# Make food
def make_food():
    global food_eaten, food_pos

    if food_eaten:
        potential_places = [
            [x, y]
            for x in range(0, size[0], grid_size)
            for y in range(0, size[1], grid_size)
            if [x, y] not in snake
        ]

        if not potential_places:
            return

        food_pos = random.choice(potential_places)
        food_eaten = False

    pygame.draw.circle(
        screen,
        FOOD_COLOR,
        (food_pos[0] + grid_size // 2,
         food_pos[1] + grid_size // 2),
        grid_size // 2 - 2
    )


# Move snake and check collision
def move_snake():
    global food_eaten, score

    x = snake[0][0] + direction[0]
    y = snake[0][1] + direction[1]

    new_pos = [x, y]
    snake.insert(0, new_pos)

    if new_pos == food_pos:
        food_eaten = True
        score += 10
    else:
        snake.pop()

    # Wall collision
    if x < 0 or x >= size[0] or y < 0 or y >= size[1]:
        return False

    # Self collision
    if new_pos in snake[1:]:
        return False

    return True


# Game over
def show_game_over():
    font = pygame.font.Font(None, 70)

    text = font.render("GAME OVER", True, FOOD_COLOR)

    screen.blit(
        text,
        (size[0] // 2 - text.get_width() // 2,
         size[1] // 2 - text.get_height() // 2)
    )

    score_text = score_font.render(
        "Final Score: " + str(score), True, TEXT_COLOR
    )

    screen.blit(
        score_text,
        (size[0] // 2 - score_text.get_width() // 2, 340)
    )

    pygame.display.flip()


# Main loop
running = True
game_over = False

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:

            if event.key == pygame.K_RIGHT and direction != [-grid_size, 0]:
                direction = [grid_size, 0]

            if event.key == pygame.K_LEFT and direction != [grid_size, 0]:
                direction = [-grid_size, 0]

            if event.key == pygame.K_UP and direction != [0, grid_size]:
                direction = [0, -grid_size]

            if event.key == pygame.K_DOWN and direction != [0, -grid_size]:
                direction = [0, grid_size]

    if not game_over:

        draw_background()
        make_food()

        alive = move_snake()

        draw_snake()

        score_render = score_font.render(
            "Score: " + str(score), True, TEXT_COLOR
        )

        screen.blit(score_render, (10, 10))

        if not alive:
            game_over = True

        pygame.display.flip()

    else:
        show_game_over()

    clock.tick(5)

pygame.quit()
