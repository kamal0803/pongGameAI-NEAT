from game import Game
import pygame

width, height = 600, 480
window = pygame.display.set_mode((width, height))
game = Game(window, width, height)

running = True

while running:

    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball_d = game.draw()
    game.detect_collision(ball_d)
    game.move_paddle()

    game.loop()
    pygame.display.flip()

pygame.quit()