import pygame
import random

successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

screen_wh = (720, 480)
screen = pygame.display.set_mode(screen_wh)
clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Apple:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, screen_wh[0] - 20), random.randint(0, screen_wh[1] - 20), 20, 20)
        #pygame.draw.rect(screen, WHITE, self.rect)
    def captured(self):
        player.length += 1*10
        self.rect = pygame.Rect(random.randint(0, screen_wh[0] - 20), random.randint(0, screen_wh[1] - 20), 20, 20)
        #pygame.draw.rect(screen, WHITE, self.rect)
        

class Player():
    def __init__(self, length):
        self.rects = [[i*5, 30] for i in range(1, 5)]
        self.length = length
        self.velocity = [0, 0]

    def update(self):
        if len(self.rects) == self.length:
            del self.rects[0]
        self.rects.append([self.velocity[i]+self.rects[-1][i] for i in range(2)])
        if self.rects[-1][0] < 0:
            self.rects[-1][0] = screen_wh[0] - 20
        elif self.rects[-1][0] > screen_wh[0]:
            self.rects[-1][0] = 0
        if self.rects[-1][1] < 0:
            self.rects[-1][1] = screen_wh[1] - 20
        elif self.rects[-1][1] > screen_wh[1]:
            self.rects[-1][1] = 0
        
        for r in self.rects:
            curr_rect = pygame.Rect(r[0], r[1], 20, 20) 
            if apple.rect.colliderect(curr_rect):
                apple.captured()
            pygame.draw.rect(screen, WHITE, curr_rect)
        pygame.draw.rect(screen, (255, 0, 0), apple.rect)
        


player = Player(7*10)
apple = Apple()
running = True
while running:
    dt = clock.tick(FPS) / 1000
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.velocity = [0, -2] 
            elif event.key == pygame.K_s:
                player.velocity = [0, 2]  
            elif event.key == pygame.K_a:
                player.velocity = [-2, 0]
            elif event.key == pygame.K_d:
                player.velocity = [2, 0]

        '''elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player.velocity[1] = 0
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                player.velocity[0] = 0'''
    
    player.update()
    pygame.display.update()

print("Exited the game loop. Game will quit...")

