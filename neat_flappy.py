import neat
import pygame
import pickle
import math
import os
from flappy_game_core import Bird, Pipe, Game
import time

CONFIG_PATH = "config-feedforward"

SURVIVAL_REWARD_PER_FRAME = 0.1
PASS_PIPE_REWARD = 5.0
COLLISION_PENALTY = -10.0

MAX_FRAMES = 10000

pygame.init()

def evaluate_genomes(genomes,config):
    clock = pygame.time.Clock()
    clock.tick(30)

    game = Game()
    game.spawn_pipes(5, 300)  # Spawn pipes once at the start
    birds = []
    nets = []
    ge = []

    for genome_id,genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        new_bird = Bird()  # Create a new bird instance for each genome
        birds.append(new_bird)
        ge.append(genome)
    
    run = True
    frame = 0
    
    while run and frame < MAX_FRAMES and len(birds) > 0:
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        game.update_pipes(game)
        
        for i, bird in enumerate(birds):
            next_pipe = bird.next_pipe

            inputs = [
                bird.position.y / game.screen.get_height(),
                bird.velocity.y / 10,
                (next_pipe.position.x - bird.position.x) / game.screen.get_width(),
                next_pipe.top_rect.bottom / game.screen.get_height(),   
                next_pipe.bottom_rect.top / game.screen.get_height()
            ]

            output = nets[i].activate(inputs)

            if output[0] > 0.5:
                bird.flap()
        
        for bird in birds:
            bird.update(game)

        for i, bird in reversed(list(enumerate(birds))):
            if bird.collided:
                ge[i].fitness += COLLISION_PENALTY
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)
                continue
            else:
                ge[i].fitness += SURVIVAL_REWARD_PER_FRAME
                
                ge[i].fitness += PASS_PIPE_REWARD * game.score
                game.score = 0
        game.update_pipes(game)
        game.update()
