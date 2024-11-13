from paddle import Paddle
from ball import Ball
from partitions import Partitions
import random
import pygame

pygame.init()

class GameInformation:
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score

class Game:

    WINNING_SCORE = 5
    SCORE_FONT = pygame.font.Font('freesansbold.ttf', 16)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.l_paddle = Paddle(Paddle.PADDLE_WIDTH, 175, Paddle.PADDLE_WIDTH, Paddle.PADDLE_HEIGHT)
        self.r_paddle = Paddle(self.window_width - Paddle.PADDLE_WIDTH*2, 175, Paddle.PADDLE_WIDTH, Paddle.PADDLE_HEIGHT)
        self.partitions = [Partitions(self.window_width/2, Partitions.PARTITION_WIDTH, Partitions.PARTITION_WIDTH, Partitions.PARTITION_HEIGHT), Partitions(self.window_width/2, Partitions.PARTITION_WIDTH + Partitions.PARTITION_DISTANCE, Partitions.PARTITION_WIDTH, Partitions.PARTITION_HEIGHT), Partitions(self.window_width/2, Partitions.PARTITION_WIDTH + 2*Partitions.PARTITION_DISTANCE, Partitions.PARTITION_WIDTH, Partitions.PARTITION_HEIGHT),
              Partitions(self.window_width/2, Partitions.PARTITION_WIDTH + 3*Partitions.PARTITION_DISTANCE, Partitions.PARTITION_WIDTH, Partitions.PARTITION_HEIGHT), Partitions(self.window_width/2, Partitions.PARTITION_WIDTH + 4*Partitions.PARTITION_DISTANCE, Partitions.PARTITION_WIDTH, Partitions.PARTITION_HEIGHT), Partitions(self.window_width/2, Partitions.PARTITION_WIDTH + 5*Partitions.PARTITION_DISTANCE, Partitions.PARTITION_WIDTH, Partitions.PARTITION_HEIGHT),
              Partitions(self.window_width/2, Partitions.PARTITION_WIDTH + 6*Partitions.PARTITION_DISTANCE, Partitions.PARTITION_WIDTH, Partitions.PARTITION_HEIGHT)]

        self.ball = Ball(self.window_width / 2, random.randint(100, 300), Ball.BALL_RADIUS)
        self.left_hits = 0
        self.right_hits = 0
        self.left_score = 0
        self.right_score = 0
        self.window = window

    def draw(self, _display_score=True):
        self.window.fill(self.BLACK)

        for paddle in [self.l_paddle, self.r_paddle]:
            paddle.draw(self.window)

        for partition in self.partitions:
            partition.draw(self.window)

        ball_d = self.ball.draw(self.window)

        if _display_score:
            self.display_score()

        return ball_d

    def move_paddle(self, left=True, up=True):

        if left:
            if up:
                self.l_paddle.move_up(Paddle.PADDLE_VELOCITY)
            else:

                self.l_paddle.move_down(Paddle.PADDLE_VELOCITY)
        else:
            if up:
                self.r_paddle.move_up(Paddle.PADDLE_VELOCITY)
            else:
                self.r_paddle.move_down(Paddle.PADDLE_VELOCITY)

        self.l_paddle.within_upper_bound()
        self.l_paddle.within_lower_bound()
        self.r_paddle.within_upper_bound()
        self.r_paddle.within_lower_bound()

    def detect_collision(self, ball_d):

        if self.ball.y + self.ball.ball_radius >= self.window_height or self.ball.y - self.ball.ball_radius <= 0:
            self.ball.ball_velocity_y *= -1

        if self.r_paddle.paddle.colliderect(ball_d):
            self.right_hits = self.right_hits + 1
            self.ball.ball_velocity_x *= -1
            diff = self.r_paddle.height // 2 - (ball_d.clip(self.r_paddle.paddle).y - self.r_paddle.y)
            reduction_factor = (self.r_paddle.height / 2) / self.ball.ball_velocity_x
            y_vel = diff / reduction_factor
            self.ball.ball_velocity_y = (-1) * y_vel

        if self.l_paddle.paddle.colliderect(ball_d):
            self.left_hits = self.left_hits + 1
            self.ball.ball_velocity_x *= -1
            diff = self.l_paddle.height // 2 - (ball_d.clip(self.l_paddle.paddle).y - self.l_paddle.y)
            reduction_factor = (self.l_paddle.height / 2) / self.ball.ball_velocity_x
            y_vel = diff / reduction_factor
            self.ball.ball_velocity_y = (-1) * y_vel

    def display_score(self):

        right_score_display = self.SCORE_FONT.render(f"Score: {self.left_score}", True, self.WHITE)
        self.window.blit(right_score_display, (150, self.window_height/10))

        left_score_display = self.SCORE_FONT.render(f"Score: {self.right_score}", True, self.WHITE)
        self.window.blit(left_score_display, (400, self.window_height/10))

    def detect_ball_miss(self):

        if self.ball.x > self.window_width - self.ball.ball_radius:
            self.left_score = self.left_score + 1
            self.ball.ball_velocity_x *= -1
            self.ball.reset()
            self.l_paddle.reset()
            self.r_paddle.reset()

        if self.ball.x - self.ball.ball_radius < 0:
            self.right_score = self.right_score + 1
            self.ball.ball_velocity_x *= -1
            self.ball.reset()
            self.l_paddle.reset()
            self.r_paddle.reset()

    def check_if_winning_score(self, running=True):

        is_game_over = False

        if self.right_score == self.WINNING_SCORE or self.left_score == self.WINNING_SCORE:
            game_over_timer = pygame.time.get_ticks()
            is_game_over = True

        if is_game_over:
            self.window.fill(self.BLACK)
            font = pygame.font.Font('freesansbold.ttf', 26)

            if self.right_score == self.WINNING_SCORE:
                winning_text = font.render(f"RIGHT WON!!", True, self.WHITE)
                self.window.blit(winning_text, (200, 200))
            else:
                losing_text = font.render("LEFT WON!!", True, self.WHITE)
                self.window.blit(losing_text, (200, 200))

            if pygame.time.get_ticks() - game_over_timer > 10000:
                running = False

        return running
    def loop(self):
        self.ball.move()
        self.detect_ball_miss()
        #self.check_if_winning_score()

        game_info = GameInformation(self.left_hits, self.right_hits, self.left_score, self.right_score)
        return game_info



