import pygame


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 25
        self.speed = 20

    def move(self, direction, screen_width, screen_height):

        # Move up
        if direction == "up":
            if self.y - self.speed - self.radius >= 0:
                self.y -= self.speed

        # Move down
        elif direction == "down":
            if self.y + self.speed + self.radius <= screen_height:
                self.y += self.speed

        # Move left
        elif direction == "left":
            if self.x - self.speed - self.radius >= 0:
                self.x -= self.speed

        # Move right
        elif direction == "right":
            if self.x + self.speed + self.radius <= screen_width:
                self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (self.x, self.y),
            self.radius
        )