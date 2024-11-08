import random
import pygame

WHITE = (255, 255, 255)


class Ball:

    def __init__(self, x, y, ball_radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.ball_radius = ball_radius

        if random.choice([True, False]):
            self.ball_velocity_x = random.randint(-10, -5)
        else:
            self.ball_velocity_x = random.randint(5, 10)

        self.ball_velocity_y = random.randint(3, 5)

    def draw(self, screen):
        ball_d = pygame.draw.circle(screen, WHITE, (self.x, self.y), self.ball_radius)
        return ball_d

    def move(self):
        self.x = self.x + self.ball_velocity_x
        self.y = self.y + self.ball_velocity_y

    def reset(self):
        self.x = self.original_x
        self.y = random.randint(100, 300)
