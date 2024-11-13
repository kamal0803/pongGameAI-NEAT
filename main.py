from game import Game
import pygame
import os
import neat
import pickle
import time

pygame.init()

class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.l_paddle = self.game.l_paddle
        self.r_paddle = self.game.r_paddle
        self.ball = self.game.ball

    def test_ai(self, net):

        #net = neat.nn.FeedForwardNetwork.create(genome, config)
        running = True

        while running:

            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            output = net.activate((self.r_paddle.y, abs(self.r_paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))

            if decision == 1:
                self.game.move_paddle(left=False, up=True)
            elif decision == 2:
                self.game.move_paddle(left=False, up=False)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            elif keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            ball_d = self.game.draw()
            self.game.detect_collision(ball_d)

            self.game.loop()
            pygame.display.flip()

        pygame.quit()

    def train_ai(self, genome1, genome2, config):

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        start_time = time.time()

        running = True
        while running:
            pygame.time.delay(25)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output1 = net1.activate((self.l_paddle.y, self.ball.y, abs(self.l_paddle.x - self.ball.x)))

            decision1 = output1.index(max(output1))

            if decision1 == 0:
                genome1.fitness = genome1.fitness - 0.01
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)

            output2 = net2.activate((self.r_paddle.y, self.ball.y, abs(self.r_paddle.x - self.ball.x)))

            decision2 = output2.index(max(output2))

            if decision2 == 0:
                genome2.fitness = genome2.fitness - 0.01
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            ball_d = self.game.draw()
            self.game.detect_collision(ball_d)

            game_info = self.game.loop()

            pygame.display.update()
            duration = time.time() - start_time
            if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits >= 50 or game_info.right_hits >= 50:
                self.calculate_fitness(genome1, genome2, game_info, duration)
                break

    def calculate_fitness(self, genome1, genome2, game_info, duration):
        genome1.fitness = genome1.fitness + game_info.left_hits + duration
        genome2.fitness = genome2.fitness + game_info.right_hits + duration


def eval_genomes(genomes, config):

    width, height = 600, 480
    window = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGame(window, width, height)
            game.train_ai(genome1, genome2, config)


def run_neat(config):

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-5')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)

    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width, height = 600, 480
    win = pygame.display.set_mode((width, height))
    pong = PongGame(win, width, height)
    pong.test_ai(winner_net)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    #run_neat(config)
    test_best_network(config)
