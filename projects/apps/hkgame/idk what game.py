import pygame
import random
import math

successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

screen_wh = (1000, 1000)
screen = pygame.display.set_mode(screen_wh)
FPS = 60
default_vel = 10
reset_dash, t = pygame.USEREVENT+1, 1000
pygame.time.set_timer(reset_dash, 0)
score = 0
pygame.display.set_caption("game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player:
    def __init__(self, x, y):
        self.img = pygame.image.load('hk-img.png')
        self.img.convert()
        self.sprite = self.img.get_rect()
        self.sprite.center = x, y
        self.x, self.y = x, y
        self.move_dict = {pygame.K_UP:1, pygame.K_DOWN:[0, default_vel], pygame.K_LEFT:[-1*default_vel, 0], pygame.K_RIGHT:[default_vel, 0]}
        self.v = [0, 0]
        self.dash = True
        self.direction = -1
        self.wings = True
        
    def update(self):
        self.x, self.y = self.x + self.v[0], self.y + self.v[1]
        if self.x > 960:
            self.x = 960
        elif self.x < 0:
            self.x = 0      
        self.sprite.center = self.x, self.y
        if self.sprite.colliderect(ground):
            self.y = 914
            self.wings = True
            self.v[1] = 0
            self.sprite.center = self.x, self.y
    
    def attack(self):
        self.img = pygame.image.load('nail-swing.png')
        self.img.convert()
        global in_swing
        in_swing = [8, True]
        if self.direction == 1:
            self.img = pygame.transform.flip(self.img, True, False)
        
    def end_attack(self):
        self.img = pygame.image.load('hk-img.png')
        self.img.convert()
        if self.direction == 1:
            self.img = pygame.transform.flip(self.img, True, False)
            
        
def main():
    player = Player(40, 914)
    global ground, in_swing
    in_swing = [8, False]  
    ground = pygame.Rect(0, 957, 1000, 43)
    while True:
        if in_swing[1]:
            in_swing[0] -= 1
            if in_swing[0] == 6:
                player.end_attack()
            elif in_swing[0] == 0:
                in_swing = [2, False]
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.v[1] = 0
                else:
                    player.v[0] = 0
            elif event.type == reset_dash:
                player.dash = True
                pygame.time.set_timer(reset_dash, 0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and player.y != 914:
                    if player.wings:
                        print('used wings')
                        player.wings = False
                        player.v[1] = -14
                        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            player.v[0] = -10
            if player.direction == -1:
                if in_swing[1]:
                    player.end_attack()
                    in_swing = [8, False]
                player.img = pygame.transform.flip(player.img, True, False)
                player.direction = 1
        if keys[pygame.K_RIGHT]:
            player.v[0] = 10
            if player.direction == 1:
                if in_swing[1]:
                    player.end_attack()
                    in_swing = [8, False]
                player.img = pygame.transform.flip(player.img, True, False)
                player.direction = -1
        if keys[pygame.K_z]:
            if player.y == 914:
                player.v[1] = -14
        else:
            player.v[1] += 2
        
        if keys[pygame.K_x]:
            if not in_swing[1]:
                player.attack()
                
        if keys[pygame.K_c] and player.dash:
            player.dash = False
            pygame.time.set_timer(reset_dash, 500)
            player.x += player.direction * 90   
                    
        player.update()
        if in_swing[0] <= 6 or not in_swing[1]:
            screen.blit(player.img, (player.x - 20, player.y - 43))
        else:
            if player.direction == 1:
                screen.blit(player.img, (player.x - 55, player.y - 125))
            else:
                screen.blit(player.img, (player.x - 200, player.y - 125))
        pygame.draw.rect(screen, WHITE, ground)
        pygame.display.update()
        pygame.time.wait(50)

if __name__ == '__main__':
    main()