import tkinter
import random
import colour
import math, random
from colour import Color

def create():
    global sy, sky_objs
    sky_objs = []
    sy += 50
    
    size = 10    
    for x in range(0, 801, size):
        for y in range(0, 801, size):
            i = int(math.dist((x, y), (400, sy))/10)
            if i > 56:
                i = 56
            c = sky_colors[i]
            sky_objs.append(canvas.create_rectangle(x, y, x + size, y + size, fill=c, outline=''))
            
    canvas.create_oval(300, sy - 100, 500, sy + 100, fill=Color('firebrick'), outline=sky_colors[2], width=5)
    ground()
    if sy < 600:
        window.after(100, create)
    else:        
        night()
    
def night():
    moon_colors = list(Color('grey').range_to(Color('black'), 57))
    size = 10
    for x in range(0, 801, size):
        for y in range(0, 395, size):
            i = int(math.dist((x, y), (600, 200))/10)
            if i > 56:
                i = 56
            c = moon_colors[i]
            canvas.create_rectangle(x, y, x + size, y + size, fill=c, outline='')   
    global stars1
    stars1 = []
    stars = [(random.randint(10, 150), random.randint(10, 70)) for _ in range(35)]
    for x, y in stars:
        while math.dist((x, y), (120, 40)) < 12:
            x, y = random.randint(10, 150), random.randint(10, 70)
        x, y = x * 5, y * 5
        stars1.append(canvas.create_rectangle(x, y, x + 3, y + 3, fill='white', outline=''))
    c = str(hex(225)[2:])
    c2 = str(hex(215)[2:])
    canvas.create_oval((550, 150, 650, 250), fill='#'+3*c, outline='#'+3*c2, width = 3)
    refresh_stars()

def refresh_stars():
    global stars1
    for a in stars1:
        canvas.delete(a)
        
    stars = [(random.randint(10, 150), random.randint(10, 70)) for _ in range(35)]
    for x, y in stars:
        while math.dist((x, y), (120, 40)) < 12:
            x, y = random.randint(10, 150), random.randint(10, 70)
        x, y = x * 5, y * 5
        stars1.append(canvas.create_rectangle(x, y, x + 3, y + 3, fill='white', outline=''))   
    
    window.after(100, refresh_stars)
    
def ground():
    for i, c in enumerate(purples):
        y = 395 + 10 * i
        canvas.create_line((0, y), (dim, y), width=10, fill=c)
            
    for i, x in enumerate(x_list):
        x1 = int(400 + -10 * (dim/2 - x))
        canvas.create_line((x1, dim), (x, 390), width=1, fill='white')
    
if __name__ == '__main__':
    window = tkinter.Tk()
    
    dim = 800
    window.geometry('{0}x{0}'.format(dim + 100))
    purples = list(Color('purple').range_to(Color('midnightblue'), 41))  
    sky_colors = list(Color('firebrick').range_to(Color('black'), 57))
    
    canvas = tkinter.Canvas(window, width=dim, height=dim, bg='black')
    canvas.pack()
    
    x_list = [x * 10 for x in range(1, 81)] 
    x_list = x_list + [x+5 for x in x_list]   
    
    sy = 0 
    create()
    window.mainloop()