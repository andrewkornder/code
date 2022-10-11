import tkinter
import random
import os
from pprint import pprint

colors = ['#111122', '#ee2244']
background = '#2211ee'

class Board:
    def __init__(self, width=7, height=6, colors=colors):
        canvas.create_rectangle(335, 100, 1050, 700, fill='#777777')
        
        self.black = colors[0]
        self.red = colors[1]
        
        self.width = width
        self.height = height
        
        self.turn = self.black
        self.arr = [[background for i in range(height)] for j in range(width)]
        self.circles = []
        self.diag_coords = get_diagonals(width, height)
        self.place = [height - 1] * width

    def press(self, event, button):
        if player:
            turn = [self.black, self.red][button]
            
        if not (350 <= event.y <= 1050):
            return
        
        x = event.y - 350
        col = int(x / size)
        row = self.place[col]
        if row == -1:
            return
        
        self.place[col] -= 1
        
        self.arr[col][row] = self.turn
        if self.check_win():
            end_game(['red', 'black'][turn == '#111122'])
            return
        if not player:
            self.turn = self.red if self.turn == self.black else self.black
        
        self.display()
     
    def display(self):
        for c in self.circles:
            canvas.delete(c)
        self.circles = []
            
        for i, column in enumerate(self.arr):
            x = i * size + 350
            x1 = x + csize
            for j, square in enumerate(column):
                y = j * size + 107
                y1 = y + csize
                self.circles.append(canvas.create_oval(x, y, x1, y1, fill=square))
                
    def check_win(self):
        diagonals = [[self.arr[x][y] for x, y in diag] for diag in self.diag_coords]
        for xy in diagonals:
            if sublist_exists(xy, [self.turn] * 4):
                return True
        
        for arr in [self.arr, self.rotate()]:
            for sublist in arr:
                if sublist_exists(sublist, [self.turn] * 4):
                    return True
        return False
    
    def rotate(self):
        return [[self.arr[j][i] for j in range(self.width)] for i in range(self.height)]
    
def get_diagonals(w, h):
    d = [[(j + i, j) for j in range(w - i)] for i in range(w)][1:]
    d += [[(j, j + i) for j in range(h - i)] for i in range(h)]
    d += [[(w - a - 1, b) for a, b in d2] for d2 in d]
    
    return d

def sublist_exists(l, sublist):
    if len(sublist) > len(l):
        return False
    for i in range(board.height-3):
        if sublist == l[i:i+4]:
            return True
    return False

def end_game(won):
    print(f'{won} won the game')
    root.destroy()

if __name__ == '__main__':
    dimX = 1400
    dimY = 800
    size = 100
    csize = 85
    
    root = tkinter.Tk()
    root.title('connect 4')
    root.geometry(f'{dimX}x{dimY}')
    
    canvas = tkinter.Canvas(root, width=dimX, height=dimY, bg=background)
    canvas.pack()
    
    board = Board()
    board.display()
    
    canvas.bind('<Button-1>', lambda event: board.press(event, 0))
    canvas.bind('<Button-3>', lambda event: board.press(event, 1))
    
    root.mainloop()