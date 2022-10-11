import tkinter
import random
from itertools import permutations
from colour import Color

colors = list(set(map(''.join, permutations('ffffff000000', 6))))

def go(event):
    '''
    add circles t times to a random canvas that is passed in.
    
    :param canvas: which canvas to add a circle to
    '''
    
    t = 1
    global recentCanvas
    recentCanvas = [canvasR, canvasL][random.randint(0, 1)]
    for _ in range(t):
        size = random.randint(10, 40)
        x = random.randint(11, 400)
        y = random.randint(11, 400)
        c = colors[random.randint(0, len(colors)-1)]
        c2 = colors[random.randint(0, len(colors)-1)]
        objects[recentCanvas].append(recentCanvas.create_oval(x, y, x + size, y + size, fill='#'+c, activefill='#'+c2))

def clear():
    '''
    clear all circles from both canvases.
    '''    
    
    global objects
    objects = {canvasR:[], canvasL:[]}
    canvasL.delete('all')
    canvasR.delete('all')
    

def clearLast():
    '''
    clear the most recently added circle
    '''
    recentCanvas.delete(objects[recentCanvas].pop())

def move(event):
    global oldxy
    canvasL.create_line(oldxy, (event.y, event.y))
    oldxy = (event.y, event.y)

def create_widgets():
    global canvasR, canvasL, canvas3, objects, recentCanvas, oldxy
    recentCanvas = None
    oldxy = (0, 0)
    
    btn = tkinter.Button(root, text='Clear Last', command=clearLast)
    btn.grid(row=0, column=1)
    btn2 = tkinter.Button(root, text='Clear', command=clear)
    btn2.grid(row=0, column=2)
    
    canvasR, canvasL, canvas3 = tkinter.Canvas(root, bg='blue', width=440, height=300), tkinter.Canvas(root, bg='red', width=440, height=300), tkinter.Canvas(root, bg='blue', width=500, height=200)
    canvasR.bind('<Button-1>', go)
    canvasL.bind('<Button-1>', go)
    #canvasL.bind('<Motion>', move)
    
    canvas3.grid(row=2, column=1)

    create_cube()
    sky()
    
    canvasR.grid(row=1, column=2)
    canvasL.grid(row=1, column=1)
    objects = {canvasR:[], canvasL:[]}
    
        
def create_window():
    global root
    root = tkinter.Tk()
    root.title('gui')
    root.geometry('900x700')
    create_widgets()
    root.mainloop()

if __name__ == '__main__':
    create_window()
