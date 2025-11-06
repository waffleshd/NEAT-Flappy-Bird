import random
import pygame

 
class Bird:
    def __init__(self):
        self.velocity = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(100, 250)

        self.flap_power = -10
        self.grav = 1

        self.next_pipe = None
        self.collided = False

    def flap(self):
        self.velocity.y = self.flap_power

    def update(self,game):
        self.velocity.y += self.grav
        self.position.y += self.velocity.y 
        if self.position.y < 0 or self.position.y > 600:
            self.collided = True  # Let the game loop handle ending the game
        self.draw()

    def draw(self):
        pygame.draw.circle(pygame.display.get_surface(), (255, 255, 0), (int(self.position.x), int(self.position.y)), 15)
        

class Pipe:
    def __init__(self):
        self.scroll_speed = -8
        self.gap_start = random.randint(100, 400)

        self.position = pygame.Vector2()

        self.pointer = None
        self.next_pipe = None

    def update(self,game):
        self.position.x += self.scroll_speed
        if self.position.x < 100:
            self.position.x = self.pointer.position.x + 300
            game.bird.next_pipe = self.next_pipe
            game.score += 1
            print(game.score)

    def draw(self,game):
        self.top_rect = pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (self.position.x, 0, 50, self.gap_start))
        self.bottom_rect = pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (self.position.x, self.gap_start + 150, 50, 600 - (self.gap_start + 150)))

        bird_rec = game.bird.rect = pygame.Rect(game.bird.position.x - 5, game.bird.position.y - 5, 10, 10)
        if bird_rec.colliderect(self.top_rect) or bird_rec.colliderect(self.bottom_rect):
            game.bird.collided = True



class Game:
    def __init__(self):
        self.pipes = []
        self.bird = Bird()
        self.screen = pygame.display.set_mode((800, 600))

        self.score = 0

        self.running = True

    def spawn_pipes(self, n, spacing):
        '''Spawns n pipes at given interval'''
        for i in range(n):
            pipe = Pipe()
            self.pipes.append(pipe)
            pipe.position.x = 800 + i * spacing
            if i > 0:
                pipe.pointer = self.pipes[i - 1]
        self.pipes[0].pointer = self.pipes[-1]
        self.bird.next_pipe = self.pipes[0]

        for i, pipe in enumerate(self.pipes):
            pipe.next_pipe = self.pipes[i+1] if i < len(self.pipes) - 1 else self.pipes[0]
       
    
    def update(self):
        self.screen.fill((135, 206, 235))  # Clear screen with sky blue color
        clock = pygame.time.Clock()
        clock.tick(30)  # Limit to 30 FPS

    def update_pipes(self,game):
        for pipe in self.pipes:
            pipe.update(game)
            pipe.draw(game)
        

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.spawn_pipes(5, 300)

    while game.running and game.bird.collided == False:
        game.update()
        game.bird.update(game)
        game.update_pipes(game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.bird.flap()
        pygame.display.flip()
        
        
    pygame.quit()

        
        