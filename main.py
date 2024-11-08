import pygame
import random
from paddle import Paddle
from partitions import Partitions
from ball import Ball

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
WIDTH, HEIGHT = 600, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
l_paddle = Paddle(PADDLE_WIDTH, 175, PADDLE_WIDTH, PADDLE_HEIGHT)
r_paddle = Paddle(WIDTH - PADDLE_WIDTH*2, 175, PADDLE_WIDTH, PADDLE_HEIGHT)

PARTITION_WIDTH, PARTITION_HEIGHT, PARTITION_DISTANCE = 10, 50, 70

partitions = [Partitions(WIDTH/2, PARTITION_WIDTH, PARTITION_WIDTH, PARTITION_HEIGHT), Partitions(WIDTH/2, PARTITION_WIDTH + PARTITION_DISTANCE, PARTITION_WIDTH, PARTITION_HEIGHT), Partitions(WIDTH/2, PARTITION_WIDTH + 2*PARTITION_DISTANCE, PARTITION_WIDTH, PARTITION_HEIGHT),
              Partitions(WIDTH/2, PARTITION_WIDTH + 3*PARTITION_DISTANCE, PARTITION_WIDTH, PARTITION_HEIGHT), Partitions(WIDTH/2, PARTITION_WIDTH + 4*PARTITION_DISTANCE, PARTITION_WIDTH, PARTITION_HEIGHT), Partitions(WIDTH/2, PARTITION_WIDTH + 5*PARTITION_DISTANCE, PARTITION_WIDTH, PARTITION_HEIGHT),
              Partitions(WIDTH/2, PARTITION_WIDTH + 6*PARTITION_DISTANCE, PARTITION_WIDTH, PARTITION_HEIGHT)]

ball = Ball(WIDTH/2, random.randint(100, 300), 10)

running = True
PADDLE_VELOCITY = 5

left_score = 0
right_score = 0

font = pygame.font.Font('freesansbold.ttf', 16)

WINNING_SCORE = 5
is_game_over = False

def detect_collision_with_paddle(paddle, ball_d):

    if paddle.paddle.colliderect(ball_d):

        if ball_d.clip(paddle.paddle).y - paddle.y < paddle.height // 2:
            ball.ball_velocity_x *= -1
            diff = paddle.height // 2 - (ball_d.clip(paddle.paddle).y - paddle.y)
            reduction_factor = (l_paddle.height / 2) / ball.ball_velocity_x
            y_vel = diff / reduction_factor
            ball.ball_velocity_y = (-1) * y_vel

        else:
            ball.ball_velocity_x *= -1
            diff = paddle.height // 2 - (ball_d.clip(paddle.paddle).y - paddle.y)
            reduction_factor = (paddle.height / 2) / ball.ball_velocity_x
            y_vel = diff / reduction_factor
            ball.ball_velocity_y = (-1) * y_vel


def detect_collision_with_wall():
    if ball.y + ball.ball_radius >= HEIGHT or ball.y - ball.ball_radius <= 0:
        ball.ball_velocity_y *= -1


def detect_ball_miss(left_score, right_score):

    if ball.x > WIDTH - ball.ball_radius:
        left_score = left_score + 1
        ball.ball_velocity_x *= -1
        ball.reset()
        l_paddle.reset()
        r_paddle.reset()

    if ball.x - ball.ball_radius < 0:
        right_score = right_score + 1
        ball.ball_velocity_x *= -1
        ball.reset()
        l_paddle.reset()
        r_paddle.reset()

    return left_score, right_score


def display_score(left_score, right_score):

    right_score_display = font.render(f"Score: {left_score}", True, WHITE)
    screen.blit(right_score_display, (150, 50))

    left_score_display = font.render(f"Score: {right_score}", True, WHITE)
    screen.blit(left_score_display, (400, 50))


while running:

    screen.fill(BLACK)
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for partition in partitions:
        partition.draw(screen)

    l_paddle.draw(screen)
    r_paddle.draw(screen)
    ball_d = ball.draw(screen)

    l_paddle.within_upper_bound()
    r_paddle.within_upper_bound()
    l_paddle.within_lower_bound()
    r_paddle.within_lower_bound()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        r_paddle.move_up(PADDLE_VELOCITY)
    if keys[pygame.K_DOWN]:
        r_paddle.move_down(PADDLE_VELOCITY)

    if keys[pygame.K_w]:
        l_paddle.move_up(PADDLE_VELOCITY)
    if keys[pygame.K_s]:
        l_paddle.move_down(PADDLE_VELOCITY)

    detect_collision_with_wall()

    detect_collision_with_paddle(r_paddle, ball_d)
    detect_collision_with_paddle(l_paddle, ball_d)
    left_score, right_score = detect_ball_miss(left_score, right_score)
    ball.move()

    display_score(left_score, right_score)

    if right_score == WINNING_SCORE or left_score == WINNING_SCORE:
        game_over_timer = pygame.time.get_ticks()
        is_game_over = True

    if is_game_over:
        screen.fill(BLACK)
        font = pygame.font.Font('freesansbold.ttf', 26)

        if right_score == WINNING_SCORE:
            winning_text = font.render(f"RIGHT WON!!", True, WHITE)
            screen.blit(winning_text, (200, 200))
        else:
            losing_text = font.render("LEFT WON!!", True, WHITE)
            screen.blit(losing_text, (200, 200))

        if pygame.time.get_ticks() - game_over_timer > 10000:
            running = False

    pygame.display.flip()

pygame.quit()
