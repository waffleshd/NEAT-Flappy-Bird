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

MAX_FRAMES = 2000 # increase / decrease this to change training duration

pygame.init()

def evaluate_genomes(genomes,config):
    #init game and pipes
    game = Game()
    game.spawn_pipes(5, 300)
    #reset lists  
    birds = []
    nets = []
    ge = []

    for genome_id,genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome,config)  # apply config to create network
        nets.append(net)
        new_bird = Bird(game)  # Create a new bird instance for each genome
        birds.append(new_bird)
        ge.append(genome)
    
    run = True
    frame = 0
    
    while run and frame < MAX_FRAMES and len(birds) > 0:
        frame += 1

        for event in pygame.event.get():    #handles if we press the quit button
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #update pipes
        game.update_pipes(game)
        
        for i, bird in enumerate(birds):
            next_pipe = bird.next_pipe


            #give input to the neural net:
            """
            Y position
            Y velocity
            Distance to next pipe (X)
            Location of top pipe
            Location of bottom pipe
            """
            inputs = [
                bird.position.y,
                bird.velocity.y / 10,
                (next_pipe.position.x - bird.position.x),
                next_pipe.top_rect.bottom,   
                next_pipe.bottom_rect.top
            ]

            #get output from neural net
            output = nets[i].activate(inputs)

            if output[0] > 0.5:
                bird.flap()
        
        for bird in birds:
            bird.update(game)

        for i, bird in reversed(list(enumerate(birds))):
            #if bird collides, penalize and remove from lists
            if bird.collided:
                ge[i].fitness += COLLISION_PENALTY
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)
                continue
            else:
                #reward for surviving each frame
                ge[i].fitness += SURVIVAL_REWARD_PER_FRAME
                
                #reward for passing pipes
                ge[i].fitness += PASS_PIPE_REWARD * game.score
                game.score = 0
        if frame % 5 == 0:  # Only update display every 5 frames during training
            game.update()
