import pygame
import random
import math
pygame.init()

dimensions = (480, 630)
screen = pygame.display.set_mode(dimensions)
FPS = 60
speed = 30
block_size = 30
score = 0
pygame.display.set_caption("TETRIS")
myfont = pygame.font.SysFont("monospace", 50)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Object:
    def __init__(self):
        self.velocity = [0, speed]
        self.x, self.y = random.randint(0, 4)*100, -30
        self.rect = pygame.Rect(self.x, self.y, block_size, block_size)
        self.color = random_color()
    
    def update(self):
        if self.y >= 600:
            pygame.draw.rect(screen, self.color, self.rect)
            return True
        if self.x < dimensions[0] - block_size and self.x >= 0:
            self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.rect = pygame.Rect(self.x, self.y, block_size, block_size)
        for x in objects[:-1]:
            if self.rect.colliderect(x.rect):
                self.y -= speed
                self.rect = pygame.Rect(self.x, self.y, block_size, block_size)
                pygame.draw.rect(screen, self.color, self.rect)              
                return True
        print(self.y)
        pygame.draw.rect(screen, self.color, self.rect)
        
        
    
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
def main():
    global objects
    objects = [Object()]
    counter = 3
    while True:
        counter -= 1
        current = objects[-1]
        if counter == 0:
            screen.fill(BLACK)            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()         
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_RIGHT:
                        current.velocity = [speed, speed]
                    elif event.key == pygame.K_LEFT:
                        current.velocity = [-1*speed, speed]
                if event.type == pygame.KEYUP:
                    current.velocity = [0, speed]
                
            for obj in objects[:-1]:
                pygame.draw.rect(screen, obj.color, obj.rect)
            if current.update():
                current.velocity = [0, 0]
                objects.append(Object())
            scoretext = myfont.render(str(score), 1, (255, 255, 255))
            screen.blit(scoretext, (5, 10))
            counter = 3
        pygame.display.update()
        pygame.time.delay(50)
        
if __name__ == '__main__':
    main()