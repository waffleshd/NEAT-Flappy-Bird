import random
import pygame

class Bird:
    def __init__(self): #initialize the bird with position, velocity, gravity, lift, and size
        self.position = pygame.Vector2(100, 250)
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 0.6
        self.lift = -8
        self.size = 20
        self.points = -3
        self.buffer = 2

    def collision(self, pipe,top_rect,bottom_rect):  #check for collision with a pipe
        bird_rect = pygame.Rect(self.position.x-self.buffer - self.size-self.buffer, self.position.y - self.size+self.buffer, (self.size-self.buffer) * 2, (self.size-self.buffer  )  * 2)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)
    
    def game_over(self):
        print("Collision! Game Over.")
        pygame.quit()
        exit()
    
    def update(self):
        self.velocity.y += self.gravity #apply gravity to velocity
        self.position.y += self.velocity.y
        if self.position.y > 480 - self.size:   #check for ground collision
            self.game_over()
        if self.position.y < 0: #check for ceiling collision
            self.game_over()    

    def draw(self, screen): #draw to screen
        pygame.draw.circle(screen, (255, 255, 0), (int(self.position.x), int(self.position.y)), self.size)

class Pipe:
    def __init__(self): #initialize pipe with position, speed, and size
        self.slide_speed = -4
        self.pointer = None
        self.position = pygame.Vector2(640, random.randint(100, 380))
        self.width = 75
        self.passed = False
        self.update_rects()

    

    def circle_back(self):  #reset pipe position to the right of the last pipe
        self.position.x = self.pointer.position.x + 300
        self.position.y = random.randint(100, 380)
        self.passed = False
        self.update_rects()

    def update_rects(self): #update pipe rectangles based on position
        self.top_rect = pygame.Rect(self.position.x, 0, self.width, self.position.y - 75)   #initialize each of the pipe rectangles
        self.bottom_rect = pygame.Rect(self.position.x, self.position.y + 75, self.width, 480 - (self.position.y + 75))

    def update(self):   #update position and rectangles
        if bird.collision(self,self.top_rect,self.bottom_rect):
            bird.game_over()

        if not self.passed and bird.position.x <= self.position.x:
            bird.points += 1
            self.passed = True
            print(bird.points)
        self.position.x += self.slide_speed
        self.update_rects()

    def draw(self, screen): #draw pipe to screen
        pygame.draw.rect(screen, (0, 255, 0), self.top_rect)
        pygame.draw.rect(screen, (0, 255, 0), self.bottom_rect)

def init_pipes(num_pipes):
    pipes = []
    for _ in range(num_pipes):
        pipes.append(Pipe())
    
    pipes[0].pointer = pipes[-1]
    for pipe in pipes[1:]:
        pipe.pointer = pipes[pipes.index(pipe)-1]
        pipe.circle_back() 
    
    return pipes
    



pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Flappy Bird AI")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()
bird = Bird()
pipes = init_pipes(3)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.velocity.y = bird.lift



    screen.fill((70, 100, 255))
    bird.update()
    bird.draw(screen)

    for pipe in pipes:
        pipe.update()
        if pipe.position.x + pipe.width < 0:
            pipe.circle_back()
        pipe.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {bird.points}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Draw FPS
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(fps_text, (500, 20))

    pygame.display.flip()
    clock.tick(60)
    
