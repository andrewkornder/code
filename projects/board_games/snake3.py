import pygame
import random
import math

successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

screen_wh = (1000, 1000)
screen = pygame.display.set_mode(screen_wh)
FPS = 60
default_vel, default_length = 20, 7
default_size = (default_vel, default_vel)
score = 0
pygame.display.set_caption("SNAKE")
myfont = pygame.font.SysFont("monospace", 16)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Apple:
    def __init__(self):
        self.apple = pygame.Rect(random.randint(0, screen_wh[0] - 100), random.randint(0, screen_wh[1] - 100), default_size[0], default_size[1])
    
    def check(self, other):
        if self.apple.colliderect(other):
            x = [random.randint(0, screen_wh[x] - 100) for x in range(2)]
            self.apple = pygame.Rect(x[0], x[1], default_size[0], default_size[1])
            return True
        return False
    
class snake:
    def __init__(self, length = default_length):
        self.length = length
        #self.objects = [[default_vel*x+50, 50] for x in range(1, length+1)]
        self.objects = [[default_vel + 50, 50]]
        self.velocity = [default_vel, 0]
    
    def update(self):  
        global score
        if self.length == len(self.objects):
            del self.objects[0]
        last = [self.objects[-1][x] + self.velocity[x] for x in range(2)]
        self.objects.append(last)
        if last in self.objects[:-1]:
            screen.fill(BLACK)
            print('GAME OVER')
            return True
        last_r = pygame.Rect(last[0], last[1], default_size[0], default_size[1])
        rects = [pygame.Rect(curr[0], curr[1], default_size[0], default_size[1]) for curr in self.objects[:-1]]
        for x in rects:
            if last_r.colliderect(x):
                screen.fill(BLACK)
                print('GAME OVER')
                return None
        rects.append(last_r)
        #print(self.objects)
        for x in range(2):
            if last[x] > screen_wh[x] - default_vel:
                self.objects[-1][x] = 0
            if last[x] < 0:
                self.objects[-1][x] = screen_wh[x] - default_vel
        for pos, c_rect in enumerate(rects):
            if point.check(c_rect):
                print(self.length)
                score += 1 
                self.length += 20
            #pygame.draw.rect(screen, BLUE, c_rect)
            color = [random.randint(0, 255) for _ in range(3)]
            pygame.draw.rect(screen, tuple(color), c_rect)
        pygame.draw.rect(screen, RED, point.apple)
        return False

player = snake(10)
point = Apple()
directions = {pygame.K_w:[0, -1*default_vel], pygame.K_s:[0, default_vel], pygame.K_a:[-1*default_vel, 0], pygame.K_d:[default_vel, 0]}
arrows = {pygame.K_UP:[0, -1*default_vel], pygame.K_DOWN:[0, default_vel], pygame.K_LEFT:[-1*default_vel, 0], pygame.K_RIGHT:[default_vel, 0]}


def main():
    global score
    player.velocity = [default_vel, 0]
    player.objects = [[default_vel*x+50, 50] for x in range(1, default_length+1)]
    point.check(point.apple)
    score = 0
    screen.fill(BLACK)
    while True:
        screen.fill(BLACK)
        old_v = player.velocity
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()         
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return None
                if event.key in directions:
                    player.velocity = directions[event.key]
                    if player.velocity == [-1*x for x in old_v]:
                        player.velocity = old_v
                elif event.key in arrows:
                    player.velocity = arrows[event.key]
                    if player.velocity == [-1*x for x in old_v]:
                        player.velocity = old_v                    
    
        if player.update():
            return None

        scoretext = myfont.render(str(score), 1, (255, 255, 255))
        screen.blit(scoretext, (5, 10))  
        
        pygame.display.update()
        pygame.time.delay(50)
         
if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                elif event.key == pygame.K_ESCAPE:
                    exit()