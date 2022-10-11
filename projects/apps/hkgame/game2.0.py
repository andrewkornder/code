import pygame
import random
import math
pygame.init()

screen_wh = (1000, 1000)
screen = pygame.display.set_mode(screen_wh)
score = 0
pygame.display.set_caption("game")
global speed, y_speed
y_speed = speed = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player:
    def __init__(self):
        self.img = pygame.image.load('hk-img.png')
        self.img.convert()
        self.sprite = self.img.get_rect()
        self.x, self.y = 40, 914
        self.direc = 1
        self.abilities = {'dash':True, 'jump':True, 'attack':True}
        self.pre_frames = {'end_move':3, 'in jump':0, 'falling':[0, 0]}
    
    def reset(self):
        self.y = 914
        self.abilities = {'dash':True, 'jump':True, 'attack':self.abilities['attack']}
        self.pre_frames['falling'] = [0, 0]
    
    def update(self):
        self.sprite.center = self.x, self.y
        if self.y >= 914:
            self.reset()
        screen.blit(self.img, (self.x - 20, self.y - 43))
    def attack(self):
        self.img = pygame.image.load('nail-swing.png')
        self.img.convert()    
        
        

def main():
    running = True
    player = Player()
    ground = pygame.Rect(0, 957, 1000, 43)
    while running:
        currentJump = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    player.pre_frames['end_move'] = 3
                elif event.key == pygame.K_z:
                    player.pre_frames['falling'][0] = 100
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    currentJump = True
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()
        
        if player.pre_frames['end_move'] > 0:
            if keys[pygame.K_RIGHT]:
                if player.direc == -1:
                    player.img = pygame.transform.flip(player.img, True, False)            
                    player.direc = 1
                player.x += int(speed * player.direc * 1/player.pre_frames['end_move'])
        
            if keys[pygame.K_LEFT]:
                if player.direc == 1:
                    player.img = pygame.transform.flip(player.img, True, False)            
                    player.direc = -1        
                player.x += int(speed * player.direc * 1/player.pre_frames['end_move'])
        else:
            player.x += speed * player.direc
            player.pre_frames['end_move'] -= 1
            
        if player.pre_frames['in jump'] > 0 and keys[pygame.K_z]:
            frame = 21 - player.pre_frames['in jump']
            if frame < 8:
                player.y -= int((y_speed + frame)/2)
            else:
                player.y -= int((y_speed + frame)/3)
            player.pre_frames['in jump'] -= 1
            if player.pre_frames['in jump'] == 1:
                player.pre_frames['falling'][0] = 100               
        else:
            if keys[pygame.K_z] and currentJump:
                if player.abilities['jump'] and player.y == 914:
                    player.y -= y_speed
                    player.abilities['jump'] = False
                    player.pre_frames['in jump'] = 20
                    
        if player.pre_frames['falling'][0] > 0:
            frame = player.pre_frames['falling']
            d = frame[1] + 1 if frame[1]%3 == 0 else frame[1] + 2
            player.y += d
            player.pre_frames['falling'] = [frame[0] - 1, d]
        
        player.update()
        pygame.draw.rect(screen, WHITE, ground)
        pygame.display.update()
        pygame.time.wait(50)        
        
        
if __name__ == '__main__':
    main()