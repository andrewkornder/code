import tkinter
from functools import partial
import random
import pygame
pygame.init()
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
) 

class snake:
    def __init__(self, xy):
        self.pixels = [xy]
        self.length = 7
        board[xy[1]][xy[0]]['bg'] = '#ff0000'
    
    def move(self, d):
        if d in ['w', 's']:
            xchange = 0
            if d == 'w':
                ychange = 1
            else:
                ychange = -1
        else:
            ychange = 0
            if d == 'd':
                xchange = 1
            else:
                xchange = -1
        newxy = [self.pixels[-1][0] + xchange, self.pixels[-1][1] - ychange]
        if newxy in self.pixels:
            for row in board:
                for n in row:
                    n['bg'] = '#000000'
            return None
        for i, c in enumerate(newxy):
            if c > pixels[2][abs(i - 1)] - 1:
                newxy[i] = 0
            elif c < 0:
                newxy[i] = pixels[2][abs(i - 1)] - 1
        self.pixels.append(newxy)            
        if board[newxy[1]][newxy[0]]['bg'] == '#0000ff':
            self.length += 1
            print('captured')
            #root.after(2000, apple)
            apple()
        if len(self.pixels) == self.length:
            ox, oy = self.pixels[0]                
            board[oy][ox]['bg'] = '#ffffff'
            del self.pixels[0]
        
        for pos, pix in enumerate(self.pixels):
            rgb = board[pix[1]][pix[0]]['bg']
            rgb = rgb.lstrip('#')
            rgb = tuple(int(rgb[i:i+2], 16) for i in (0, 2, 4))
            rgb = tuple([p - i * 30 if p <= 255 and p >= 50 else p for p in rgb])
                
            board[pix[1]][pix[0]]['bg'] = '#%02x%02x%02x' % rgb
            
        board[newxy[1]][newxy[0]]['bg'] = '#ff0000'
            
def apple():
    pos = (random.randint(0, pixels[2][0] - 1), random.randint(0, pixels[2][1] - 1))
    board[pos[0]][pos[1]]['bg'] = '#0000ff'
    
def create_window(colors, start):
    global board, snake_color, default_color, root
    default_color, snake_color = colors
    window_dim, pixel_size, pixel_dim = pixels
    root = tkinter.Tk()
    root.geometry(window_dim)
    board = [[tkinter.Canvas(root, bg=default_color, width=pixel_size[0], height=pixel_size[1], highlightthickness=0) for _ in range(pixel_dim[1])] for _ in range(pixel_dim[0])]
    x, y = oldx, oldy = start
    snek = snake(start)
    '''root.bind('<w>', lambda w: snek.move('w'))
    root.bind('<s>', lambda s: snek.move('s'))
    root.bind('<a>', lambda a: snek.move('a'))
    root.bind('<d>', lambda d: snek.move('d'))
    root.bind('<Up>', lambda w: snek.move('w'))
    root.bind('<Down>', lambda s: snek.move('s'))
    root.bind('<Left>', lambda a: snek.move('a'))
    root.bind('<Right>', lambda d: snek.move('d'))'''
    for rown, row in enumerate(board):
        for coln, sq in enumerate(row):
            sq.grid(row = rown, column = coln, padx = 0, pady = 0)
    
    board[y][x]['bg'] = snake_color
    root.after(1000, apple)
    root.mainloop()
    keys = {K_DOWN:'s', K_LEFT:'a', K_RIGHT:'d', K_UP:'w'}
    while True:
        key = pygame.event.get()
        snek.move(key)
        

global pixels

size = 10
pixel_wh = (30, 30)
pixels = (str(size*pixel_wh[0])+'x'+str(size*pixel_wh[1]), (size, size), pixel_wh)
colors = ('#ffffff', '#ff0000')
create_window(colors, [5, 5])