#!/usr/bin/python
#chess3.0.py

__author__ = "Andrew Kornder"
__version__ = '1.1'

import tkinter as tk
from pprint import pprint
import classes as c

class piece():
    canvasimg = ''
    def __init__(self, y, b):
        self.color = y[1]
        self.obj = y[0]
        self.canvas = tk.Canvas(root, bg = b, width=100, height=100)
        self.fn = self.obj+self.color+'.png'
        self.img = tk.PhotoImage(file = 'imgs\\'+self.fn)

def create_window():
    c.create()
    global root, images
    root = tk.Tk()
    root.title("CHESS") 
    root.geometry("1500x1080")
    root.configure(background='black')
    images = [[None for x in range(8)] for y in range(8)]
    
    global entry, start_turn, get_check, checkmate_quit
    start_turn = tk.Button(text='enter', command=turn)
    entry = tk.Entry(width = 8)
    get_check = tk.Button(text='check', command=print_check)
    checkmate_quit = tk.Button(root, text='done', command=root.destroy)
    
    get_check.grid(row = 1, column = 9)
    entry.grid(row=9, column=0)
    start_turn.grid(row=9, column=1)
    
    global c_n, n_c, curr_turn, turn_display, king_loc, threats
    threats = []
    c_n = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}
    n_c = {v:k for k, v in c_n.items()}
    curr_turn = True
    turn_display = tk.Label(root, text='turn: '+['black', 'white'][curr_turn])
    turn_display.grid(row=9, column=3)
    king_loc = {'w' : [1, 5], 'b' : [8, 5]}
    
    refresh()
    root.mainloop()

def from_not(string):
    p = string[0]
    m = string[1:]
    #not finished
    
def get_text():
    a = [i for i in c.board.values()]
    text = {}
    for x in range(len(a)):
        text[x+1] = [(i.obj, i.color) for i in a[x].values()]
    return text
    
def refresh(checkmate = False, a = 9, b = 9):
    root.bind("<Return>", start_turn['command'])
    t = get_text()
    colors = ['#bbbbbb', '#8f8f8f']
    for x, p in enumerate(t.values()):
        for y, q in enumerate(p):
            if not checkmate:
                ci = images[x][y] = piece(q, colors[(x+y)%2])
            else:
                ci = images[x][y]
            ci.canvasimg = ci.canvas.create_image(51, 51, image=ci.img)
    if a != 9:
        images[8 - a][b-1].canvas['bg'] = '#00ff00'
    for x, p in enumerate(images):
        for y, q in enumerate(p):
            q.canvas.grid(column = y, row = x)
            bxy = c.board[x+1][y+1]
            if len(bxy.color) >= 3:
                bxy.color = bxy.color[:1]
    if checkmate:
        print('finishing')
        input()
        exit()
        root.mainloop()
    turn_display['text'] = 'turn: '+['black', 'white'][curr_turn]
    if start_turn['text'] == 'move':
        for k, v in king_loc.items():
            Cking = c.board[v[0]][v[1]]
            if Cking.color != k:
                Cking.color = k
                print(k, 'is in check')    

def to_notation(l, name):
    a = [x[::-1] for x in l]
    for index, pre in enumerate(a):
        pre[0] = n_c[pre[0]]
        if name != 'p':
            pre = name.upper() + pre
    return ', '.join([''.join(map(str, b)) for b in a])

def in_check():
    #loc = king_loc[['b', 'w'][curr_turn]]
    threats = []
    for row in c.board.values():
        for square in [a for a in row.values() if a.obj != '_']:
            if 'k' in square.moves()[1]:
                threats.append(square.square)
    
    return len(threats)>0, threats

def print_check():
    boolean, t = in_check()
    try:
        notes = to_notation(c.board[fx][fy].moves()[0], 'p')
        print('moves for '+to_notation([fx, fy], 'p')[0]+': '+notes+'\nmoveset: ', end = '')
        print(to_notation([moveset], 'p')) 
    except:
        get_out(['w', 'b'][not curr_turn])
    
    print('in check:', boolean)
    

def pprintboard(b):
    for row, r in b.items():
        print(row, end='  ')
        for s in r.values():
            try:
                print(s.obj+s.color[0].upper(), end=' ')
            except:
                print(s, end=' ')
        print()
    
def get_out(color):
    global king_loc
    out = [[], []]
    for row in range(8, 0, -1):
        for sq in c.board[row].values():
            if sq.color[0] == color[0]:
                co = c.types[sq.obj](sq.square, sq.color)
                oldK = king_loc[color][:]
                for move in co.moves()[0]:
                    board2 = {k:{k2:v2 for k2, v2 in v.items()} for k, v in c.board.items()}
                    x, y = co.square
                    c.board[x][y] = c.square((x,y))
                    co.square = c.board[move[0]][move[1]].square
                    if co.obj[0] == 'k':
                        king_loc[color] = co.square                
                    c.board[move[0]][move[1]] = co
                    check_bool, threats = in_check()
                    if not check_bool:
                        out[0].append(tuple(move))
                        out[1].append(sq.square)
                    king_loc[color] = oldK[:]
                    c.board = {k:{k2:v2 for k2, v2 in v.items()} for k, v in board2.items()}
    if len(out) == 0:
        on_checkmate()      
        
    #print('\n\npossible moves from get_out():')
    #pprint(out)
    #print()
    return out

def turn():
    global moveset, fx, fy, curr_turn, threats, fromset
    if len(threats) != 0:
        fx, fy = king_loc[['b', 'w'][curr_turn]]
        c_piece = c.board[fx][fy]
        o_moveset = get_out(['b', 'w'][curr_turn])      
        moveset = [list(move) for move in o_moveset[0]], c_piece.moves()[0]
        fromset = [move for move in o_moveset[1]]
    f = entry.get()
    if len(f)<2:
        print('too short of an input')
        return None    
    fx, fy = [int(x) if x not in c_n else c_n[x] for x in f[::-1]]
    entry.delete(0, len(f)+1)
    if len(threats) != 0:
        if (fx, fy) not in fromset:
            print('invalid starting square')
            #print(fromset, [fx, fy])
            return None
    
    c_piece = c.board[fx][fy]
    if c_piece.obj == '_': 
        print('invalid move')
        return None
    if c_piece.color[0] != ['b', 'w'][curr_turn]:
        print('wrong color')
        return None
    if len(threats) == 0:
        moveset = c_piece.moves()[0]
        moveset = moveset, moveset
    start_turn['command'] = turn2
    start_turn['text'] = 'move' 
    for i, m in enumerate(moveset[0]):
        mx, my = m
        cu = c.board[mx][my]
        addback = []
        if len(threats) != 0:
            if fromset.index((fx, fy)) == i:
                fromset[i] = None
                addback.append([i, (fx, fy)])
                cu.color += 'poss'
        #elif cu.obj == '_':
        else:
            cu.color += 'poss'
        for x in addback:
            fromset.insert(x[0], x[1])
    refresh(False, fx, fy)
    curr_turn = not curr_turn

def on_checkmate():
    print('checkmate: '+['black', 'white'][curr_turn]+' wins')
    for x in [entry, start_turn, get_check,  turn_display]:
        x.destroy()
    images[3][2].img = tk.PhotoImage(file='imgs\\checkmate.png')
    checkmate_quit.grid(row=9, column=0)
    refresh(True)
    
    
def turn2():
    global threats
    t = entry.get()
    if len(t)<2:
        print('too short of an input')
        return None
            
    tx, ty = [int(x) if x not in c_n else c_n[x] for x in t[::-1]]
    entry.delete(0, len(t)+1) 
    if [tx, ty] not in moveset[0]:
        print('not legal move')
        return None     
    c_piece = c.board[fx][fy]
    if len(threats) != 0 and c_piece.square not in fromset:
        print('not legal starting square\n', c_piece.square)
        return None          
    c.board[fx][fy] = c.square(c_piece.square)
    n_piece = c.board[tx][ty]
    c.board[tx][ty] = c_piece
    c_piece.square = n_piece.square
    del n_piece
    refresh()
    if c_piece.obj == 'p':
        c_piece.has_moved = True
    start_turn['command'] = turn
    start_turn['text'] = 'enter'
    print('\n\nmoves: '+', '.join(map(str, moveset[0])), '\nif in check: '+', '.join(map(str, moveset[1])))
    for m in moveset[1]:
        cm = c.board[m[0]][m[1]]
        if cm.obj == '_':
            cm.color = '_'
    check, threats = in_check()
    if check:
        x, y = king_loc[['b', 'w'][curr_turn]]
        c.board[x][y].color += 'C'
    else:
        x, y = king_loc[['b', 'w'][curr_turn]]
        if c.board[x][y].color[-1] == 'C':
            c.board[x][y].color = c.board[x][y].color[:-1]
    print('threat on', threats)    
    refresh()
    
if __name__ == '__main__':
    create_window()