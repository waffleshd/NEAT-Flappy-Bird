# NEAT-Flappy-Bird

This project was used to practice neural net implementation for the game flappy bird.
[Disclaimer]: I used Copilot and ChatGPT for bug fixes, and to walk me through how to implement a NEAT algorithm using the NEAT lib.

## How to use:

First, import the entire folder to your device. Make sure all .py and text files are there!

**config-feedforward** - Here, you may adjust the starting parameters for the neural nets. Most parameters don't need to be changed, however you can change the pop_size to whatever you like. It may make sense to adjust the value depending on the processing power of your computer. Decreasing pop size would also decrease training time.

**run_neat.py** - This is the main file you will want to worry about. Either run the file through your preferred IDE, or execute it via terminal. This will train your neural net for a certain amount of generations, which you can adjust in the code : NUMBER_OF_GENERATIONS. The higher the number, the longer the training will take. Just remember that improvement tends to plateau at a certain point.

**watch_winner.py** - Here, you can watch the best genome we trained play flappy bird in real time. Unless I have changed the file, a pre-trained neural net should already be in "best_bird.pkl". However, it will be overwritten once you train it yourself. Run it as you would any other .py file.

**flappy_game_core.py** - Maybe you think you are better than the algorithm :P Run this file and you can play flappy bird (the temu version) yourself!


## Dependencies

To run this, you must have pygame and neat-python installed:

Pygame installation: https://www.pygame.org/news

Neat-Python installation: https://neat-python.readthedocs.io/en/latest/installation.html

