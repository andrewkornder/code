import pygame
import random
import math
import os
import threading

pygame.init()
is_playing = 0
def play_sound():
    global is_playing
    while True:
        if is_playing == 1:
            pass
            is_playing = 0
        pygame.time.wait(50)
        
sound = threading.Thread(target=play_sound)

dim = 1000
screen = pygame.display.set_mode((dim, dim))
score = 0
reset_attack = pygame.USEREVENT+1
allow_attack = pygame.USEREVENT+2
reset_dash = pygame.USEREVENT+3
allow_dash = pygame.USEREVENT+4
end_wings = pygame.USEREVENT+5

pygame.display.set_caption("game")
global speed, gravity
gravity = 20
speed = 8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player:
    def __init__(self):
        self.x, self.y = 40, dim-68
        self.img = pygame.image.load('hk-img.png')
        self.img.convert()
        self.img = pygame.transform.flip(self.img, True, False)
        self.hitbox = self.img.get_rect()
        self.v = 0
        self.d = -1
        self.jumping = False
        self.falling = False
        self.wings = True
        self.swing = True
        self.dash = True
        self.in_dash = False
        self.in_wings = False
        self.in_swing = [False, False]
        self.health = 5
    
    def update(self):
        if not self.in_dash:
            if self.falling:
                if self.jumping:
                    self.jumping = False
                    self.y += int(gravity/2)
                else:
                    self.y += gravity
            elif self.jumping:
                if self.y < jumped_from - 300:
                    self.falling = True
                else:
                    self.y -= gravity
            
            self.x += self.v
        else:
            if self.jumping:
                self.falling = True
            self.x += self.d * 20
        if self.y >= dim-86:
            self.y = dim-86
            self.wings = True
            self.falling, self.jumping = False, False
        if self.x > dim:
            self.x = 0
        elif self.x < 0:
            self.x = dim
        if self.in_swing[0]:
            dx = 127 - self.d * 72 + self.in_swing[1] * 17
            if self.d == -1 and self.in_swing[1]:
                dx -= 140
            dy = 125 + self.in_swing[1] * 55
        elif self.in_dash:
            dx, dy = 55, 35
        elif self.in_wings:
            dx, dy = 125 + self.d * -5, 92
        else:
            dx, dy = 20, 43
        screen.blit(self.img, (self.x - dx, self.y - dy))     

    def attack(self, up):  
        global radiance
        if not up:
            self.img = pygame.image.load('nail-swing.png')
        else:
            
            self.img = pygame.image.load('hk-upswing.png')
            
        self.img.convert()
        
        self.swing = False
        pygame.time.set_timer(reset_attack, 350)
        if self.d == -1:
            self.flip_image()
    
        self.hitbox = self.img.get_rect()
        self.hitbox.center = self.x + self.d * (not up) * 20, self.y + up * -30
            
        if self.hitbox.colliderect(radiance.hitbox) and self.in_swing:
            radiance.health -= 32
        self.in_swing = [True, up]    
    def end_attack(self):
        self.in_swing[0] = False
        
        self.img = pygame.image.load('hk-img.png')
        self.img.convert()
        
        self.hitbox = self.img.get_rect()
        self.hitbox.center = self.x, self.y         
        
        pygame.time.set_timer(reset_attack, 0)
        pygame.time.set_timer(allow_attack, 100)
        if self.d == -1:
            self.flip_image()
    def end_wings_func(self):
        self.in_wings = False
        
        self.img = pygame.image.load('hk-img.png')
        self.img.convert()
        self.hitbox = self.img.get_rect()
        self.hitbox.center = self.x, self.y         
        
        pygame.time.set_timer(end_wings, 0)
        if self.d == -1:
            self.flip_image()
            
    def use_dash(self):        
        self.img = pygame.image.load('hk-dash.png')
        self.img.convert()
        self.dash = False
        self.in_dash = True
        pygame.time.set_timer(reset_dash, 150)
        if self.d == -1:
            self.flip_image()
        self.hitbox = self.img.get_rect()
        self.hitbox.center = self.x, self.y         
            
    def end_dash(self):        
        self.img = pygame.image.load('hk-img.png')
        self.img.convert()
        self.in_dash = False
        
        pygame.time.set_timer(reset_dash, 0)
        pygame.time.set_timer(allow_dash, 600)
        if self.d == -1:
            self.flip_image()
    
        self.hitbox = self.img.get_rect()
        self.hitbox.center = self.x, self.y  
        
    def flip_image(self):
        self.img = pygame.transform.flip(self.img, True, False)
        if self.in_swing[0]:
            self.end_attack()

class Boss:
    def __init__(self):
        self.name = 'Radiance'
        self.attacks = {}
        self.x, self.y = 82, 100
        self.health = 100
        self.hitbox = pygame.Rect(self.x + 262, self.y + 206, 320, 203)
        self.img = pygame.image.load('hk-radiance.png')
        self.font = pygame.font.SysFont(None, 24)
        self.img.convert()
        self.phase = 1
        
    def update(self):
        if self.health < 1:
            self.font = pygame.font.SysFont(None, 100)
            img = self.font.render('YOU WIN', True, RED)
            screen.blit(img, (dim/2 - 200, dim/2))
        else:
            img = self.font.render('health: '+str(self.health)+'/3000', True, WHITE)
            screen.blit(img, (20, 20))     
            screen.blit(self.img, (self.x, self.y))
        
def main():
    sound.start()
    running = True
    global radiance
    radiance = Boss()
    player = Player()
    global ground, jumped_from
    jumped_from = dim-86
    ground = pygame.Rect(0, dim-43, dim, 43)
    groundimg = pygame.image.load('hk-floor.png')
    groundimg.convert()
    while running:
        currentJump = False
        currentAttack = False
        currentDash = False
        oldDir = player.d
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == reset_attack:
                player.end_attack()
            elif event.type == end_wings:
                player.end_wings_func()            
            elif event.type == allow_attack:
                player.swing = True
                pygame.time.set_timer(allow_attack, 0)
            elif event.type == reset_dash:
                player.end_dash()
            elif event.type == allow_dash:
                player.dash = True
                pygame.time.set_timer(allow_dash, 0)            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    player.falling = True
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    player.v = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: 
                    currentJump = True
                if event.key == pygame.K_x:
                    currentAttack = True
                if event.key == pygame.K_c:
                    currentDash = True
                
        screen.fill(BLACK)
        if not player.in_dash:
            keys = pygame.key.get_pressed()
        
            if keys[pygame.K_z]:
                if player.falling and player.wings and currentJump:
                    jumped_from = player.y + 100
                    player.in_wings = True
                    player.img = pygame.image.load('hk-wings.png')
                    player.img.convert()
                    
                    pygame.time.set_timer(end_wings, 150)
                    if player.d == 1:
                        player.flip_image()
                    player.jumping, player.falling, player.wings = True, False, False
                    
                elif not player.falling and currentJump:
                    player.jumping = True
            
            if keys[pygame.K_RIGHT]:
                player.v = speed
                player.d = 1
            
            if keys[pygame.K_LEFT]:
                player.v = -1 * speed
                player.d = -1
            
            if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                player.v = 0 
            
            if keys[pygame.K_x] and currentAttack and player.swing and not player.in_wings:
                player.attack(keys[pygame.K_UP])       
            if keys[pygame.K_c] and currentDash and player.dash:
                player.use_dash()        
            if player.d != oldDir:
                player.flip_image()            
        
        radiance.update()
        
        player.update()
        screen.blit(groundimg, (0, dim-50))
        pygame.display.update()
        pygame.time.wait(25)         
        
if __name__ == '__main__':
    main()