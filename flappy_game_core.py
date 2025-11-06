import random
import pygame

 
class Bird:
    def __init__(self, game):       # init bird properties
        self.velocity = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(100, 250)

        self.flap_power = -10
        self.grav = 1
 
        self.next_pipe = game.pipes[0]
        self.collided = False

    def flap(self):
        self.velocity.y = self.flap_power

    def update(self,game):
        #apply grav and then update position
        self.velocity.y += self.grav
        self.position.y += self.velocity.y 

        #Handle collision with ground and ceiling
        if self.position.y < 0 or self.position.y > 600:
            self.collided = True 

        #handles collision with pipes
        bird_rec = pygame.Rect(self.position.x - 5, self.position.y - 5, 10, 10)
        if bird_rec.colliderect(self.next_pipe.top_rect) or bird_rec.colliderect(self.next_pipe.bottom_rect):
            self.collided = True

        #check if we passed a pipe
        self.check_pass(game)
        self.draw()

    
    def check_pass(self,game):
        #if we pass a pipe, change pointer to the next pipe and increase score
        if self.position.x > self.next_pipe.position.x + 50:
            self.next_pipe.position.x = self.next_pipe.pointer.position.x + 300
            self.next_pipe = self.next_pipe.next_pipe
            game.score += 1

    def draw(self):
        pygame.draw.circle(pygame.display.get_surface(), (255, 255, 0), (int(self.position.x), int(self.position.y)), 15)
        

class Pipe:
    def __init__(self): #init pipe properties
        self.scroll_speed = -8
        self.gap_start = random.randint(100, 400)

        self.position = pygame.Vector2()

        self.pointer = None
        self.next_pipe = None

    def update(self,game):  #move pipe left
        self.position.x += self.scroll_speed
        

    def draw(self,game):    #draw pipe segments
        self.top_rect = pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (self.position.x, 0, 50, self.gap_start))
        self.bottom_rect = pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (self.position.x, self.gap_start + 150, 50, 600 - (self.gap_start + 150)))

        



class Game:
    def __init__(self):  #init game properties
        self.pipes = []
        self.screen = pygame.display.set_mode((800, 600))
        self.bird = None
        self.score = 0

        self.running = True

    def spawn_pipes(self, n, spacing):
        '''Spawns n pipes at given interval'''


        for i in range(n):
            pipe = Pipe()
            self.pipes.append(pipe) #append each pipe to pipes list
            pipe.position.x = 800 + i * spacing #space pipes evenly
            if i > 0:
                pipe.pointer = self.pipes[i - 1]    #apply pointers to each pipe
        self.pipes[0].pointer = self.pipes[-1]
        

        for i, pipe in enumerate(self.pipes):   #apply next pointer so that bird can cycle through pipes
            pipe.next_pipe = self.pipes[i+1] if i < len(self.pipes) - 1 else self.pipes[0]
       
    
    def update(self):
        self.screen.fill((135, 206, 235))  # Clear screen with sky blue color
        

    def update_pipes(self,game):   
        for pipe in self.pipes:
            pipe.update(game)
            pipe.draw(game)
        

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.spawn_pipes(5, 300)
    game.bird = Bird(game)

    while game.running and game.bird.collided == False:
        game.update()
        game.update_pipes(game)
        game.bird.update(game)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.bird.flap()
        pygame.display.flip()
        
        
    pygame.quit()

        
        