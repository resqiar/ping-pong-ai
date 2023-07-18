import pygame
from pong import Game
import neat
import os
import pickle

class Agent:
    def __init__(self, window, width, height) -> None:
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    def play_agent(self, genome, config):
        # create neural network for saved genome
        network = neat.nn.FeedForwardNetwork.create(genome, config)

        running = True

        # framerate controller
        clock = pygame.time.Clock()

        while running:
            clock.tick(60) # 60 FPS at MAX

            self.game.loop()
            self.game.draw(draw_score=True, draw_hits=False)
            pygame.display.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            elif keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)

            # Let AI control right paddle
            output = network.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
# decision based on output
            decision = output.index(max(output))

            # 0 = Stay still
            # 1 = Move up
            # 2 = Move Down
            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

        pygame.quit()
    
    def train(self, genome_1, genome_2, config):
        # create neural network for each genomes
        network_1 = neat.nn.FeedForwardNetwork.create(genome_1, config)
        network_2 = neat.nn.FeedForwardNetwork.create(genome_2, config)

        running = True
        while running:
            # pass the input consistently to neural network
            # inputs needed: paddle Y, ball Y, and absolute distance of paddle - ball
            output_1 = network_1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            output_2 = network_2.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))

            # print(output_1, output_2)

            # decision based on output
            decision_1 = output_1.index(max(output_1))
            decision_2 = output_2.index(max(output_2))

            # 0 = Stay still
            # 1 = Move up
            # 2 = Move Down
            if decision_1 == 0:
                pass
            elif decision_1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)

            if decision_2 == 0:
                pass
            elif decision_2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)

            # run the game
            global_info = self.game.loop()
            self.game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()

            # define how it ended, calculate genome's fitness
            if global_info.left_score >= 1 or global_info.right_score >= 1 or global_info.left_hits > 50:
                self.grade_fitness(genome_1, genome_2, global_info)

                # immediately break the training
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
    
    def grade_fitness(self, genome_1, genome_2, global_info):
        genome_1.fitness += global_info.left_hits
        genome_2.fitness += global_info.right_hits

def eval_genomes(genomes, config):
    WIDTH, HEIGHT = 700, 500
    FRAME = pygame.display.set_mode((WIDTH, HEIGHT))

    for i, (_, genome_1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        
        genome_1.fitness = 0

        # execute current genome with any other genomes
        for _, genome_2 in genomes[i + 1:]:
            genome_2.fitness = 0 if genome_2.fitness == None else genome_2.fitness

            agent = Agent(FRAME, WIDTH, HEIGHT)
            agent.train(genome_1, genome_2, config)

def execute_neat(config):
    # load checkpoint
    save = neat.Checkpointer.restore_checkpoint('neat-checkpoint-12')

    # create a population
    population = neat.Population(config)

    # report data on screen
    # population.add_reporter(neat.StdOutReporter)
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # create a checkpoint after x generation
    population.add_reporter(neat.Checkpointer(1))

    winner = population.run(eval_genomes, 20) # 50 is the maximum generations

    # dump best genome into savefile
    with open("best_genome.pickle", "wb") as file:
        pickle.dump(winner, file)

def execute_agent(config):
    WIDTH, HEIGHT = 700, 500
    FRAME = pygame.display.set_mode((WIDTH, HEIGHT))

    with open("best_genome.pickle", "rb") as file:
        winner = pickle.load(file)

    game = Agent(FRAME, WIDTH, HEIGHT)
    game.play_agent(winner, config)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    neat_config = os.path.join(local_dir, "config.txt")

    # load neat configurations
    config = neat.Config(
                neat.DefaultGenome,
                neat.DefaultReproduction,
                neat.DefaultSpeciesSet,
                neat.DefaultStagnation,
                neat_config
            )

    # train the agent
    execute_neat(config)

    # play with the agent
    execute_agent(config)

