import pygame
from paddle import Paddle

WHITE = (255, 255, 255)


class Partitions(Paddle):

    PARTITION_WIDTH, PARTITION_HEIGHT, PARTITION_DISTANCE = 10, 50, 70

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.paddle)