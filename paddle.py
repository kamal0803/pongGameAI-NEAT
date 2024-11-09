import pygame
RED = (255, 0, 0)



class Paddle:

    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
    PADDLE_VELOCITY = 5

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        self.paddle = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.paddle)

    def within_lower_bound(self):
        if self.paddle.y > 375:
            self.paddle.update(self.paddle.x, 375, self.width, self.height)

    def within_upper_bound(self):
        if self.paddle.y < 5:
            self.paddle.update(self.paddle.x, 5, self.width, self.height)

    def move_up(self, vel):
        self.y = self.y - vel
        self.paddle.y = self.y

    def move_down(self, vel):
        self.y = self.y + vel
        self.paddle.y = self.y

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.paddle.update(self.x, self.y, self.width, self.height)
