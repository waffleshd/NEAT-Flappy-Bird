import pickle
import neat
import pygame
from flappy_game_core import Bird, Pipe, Game

config_path = "config-feedforward"
config = neat.Config(neat.DefaultGenome, 
                    neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, 
                    neat.DefaultStagnation, 
                    config_path)

"""
Next section here has a ton of debug stuff which we can ignore if everything is working fine
"""

try:
    with open("best_bird.pkl", "rb") as f:
        winner = pickle.load(f)
    print("Successfully loaded winner genome:", winner)
    print("Number of nodes:", len(winner.nodes))  # Debug genome structure
    print("Number of connections:", len(winner.connections))
    
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    print("Neural network created:", net)  # Debug network creation

    # Test network with some sample inputs
    test_inputs = [0.5, 0.0, 0.8, 0.3, 0.7]  # Sample normalized inputs
    test_output = net.activate(test_inputs)
    print("Test network output:", test_output)  # Debug network response
except Exception as e:
    print("Error loading winner or creating network:", e)
    exit()
    exit()

# Create neural network from the loaded genome
net = neat.nn.FeedForwardNetwork.create(winner, config)

#init game variables

game = Game()
game.spawn_pipes(5, 300)
bird = Bird(game) 
bird.next_pipe = game.pipes[0]  # Set initial next pipe

clock = pygame.time.Clock()

while game.running and bird.collided == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

    game.update()
    game.update_pipes(game)
    bird.update(game)


    next_pipe = bird.next_pipe


    # give input to the neural net:
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

    output = net.activate(inputs)
    #print(f"Network output: {output[0]}, Inputs: {inputs}")  # Debug output
    if output[0] > 0.5:
        bird.flap()
        
    clock.tick(60)
    pygame.display.flip()