import neat
import pickle
from neat_flappy import evaluate_genomes, CONFIG_PATH

NUMBER_OF_GENERATIONS = 50  # Adjust the number of generations as needed

def run_neat():
    #import config
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        CONFIG_PATH
    )

    # Create the population
    p = neat.Population(config)

    # Add reporters to show progress
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 50 generations (adjust as needed)
    winner = p.run(evaluate_genomes, NUMBER_OF_GENERATIONS)

    with open("best_bird.pkl", "wb") as f:
        pickle.dump(winner, f)  #dump the best genome to a file

    print("\nBest genome:\n{!s}".format(winner))

if __name__ == "__main__":
    run_neat()