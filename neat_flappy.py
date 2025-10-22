import neat
import pygame
import pickle
import math
import os
from flappy_game_core import Bird, Pipe, Game

CONFIG_PATH = "config-feedforward.txt"

SURVIVAL_REWARD_PER_FRAME = 0.1
PASS_PIPE_REWARD = 5.0
COLLISION_PENALTY = -10.0

MAX_FRAMES = 10000

def evaluate_genomes(genomes,config):

    game = Game()
    birds = []
    nets = []
    ge = []

    for genome_id,genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        birds.append(game.bird)
        ge.append(genome)
    
    clock = pygame.time.Clock()
    run = True
    frame = 0
    
    while run and frame < MAX_FRAMES and len(birds) > 0:
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        for i, bird in enumerate(birds):
            pass