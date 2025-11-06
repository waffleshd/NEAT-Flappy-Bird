import pickle
import neat
import pygame
from flappy_game_core import Bird, Pipe, Game

with open("best_bird.pkl", "rb") as f:
    winner = pickle.load(f)

config_path = "config-feedforward"
config = neat.Config(neat.DefaultGenome, 
                     neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, 
                     neat.DefaultStagnation, 
                     config_path)

net = neat.nn.FeedForwardNetwork.create(winner, config)

game = Game()
game.spawn_pipes(5, 300)

clock = pygame.time.Clock()

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    game.update()
    game.bird.update(game)
    game.update_pipes(game)

    next_pipe = game.bird.next_pipe

    inputs = [
        game.bird.position.y / game.screen.get_height(),
        game.bird.velocity / 10,
        (next_pipe.position.x - game.bird.position.x) / game.screen.get_width(),
        next_pipe.top_rect.bottom / game.screen.get_height(),   
        next_pipe.bottom_rect.top / game.screen.get_height()
    ]

    output = net.activate(inputs)
    if output[0] > 0.5:
        game.bird.flap()

    clock.tick(30)
    pygame.display.flip()