from math import dist


class Player:
    def __init__(self, game):
        self.game = game
        self.canvas = game.canvas
        
        self.x, self.y = game.center
        self.mx, self.my = game.center
        self.speed = 10
        self.moving = False
        
        self.weapon = Weapon(self, game)
        self.projectiles = []
        
        self.hp = 5
        
        self.has_dash = False
        self.dash_size = 50
        
    def get_movement(speed):
        sx, sy = self.y - self.mx, self.y - self.my
        unit = speed / (abs(sx) + abs(sy)) 
        return unit * sx, unit * sy
        
    def fire(self):
        self.projectiles += self.weapon.fire()
        
    def update_projectiles(self):
        for proj in self.projectiles:
            proj.update()
    
    def dash(self):
        dx, dy = self.get_movement(self.dash_size)
        self.x += dx
        self.y += dy
        self.canvas.moveto(self.drawing, self.x, self.y)
        
    def update(self):
        dx, dy = self.get_movement(self.speed)
        self.x += dx
        self.y += dy
        self.canvas.moveto(self.drawing, self.x, self.y)
        
        for bullet in self.projectiles:
            bullet.update()
    
class Weapon:
    def __init__(self, player, game):
        self.spread = 90
        self.bullets = 1
        self.damage = 1
        
        self.player = player
        self.game = game

    def fire(self):
        return []