import tkinter
import random
import colour

def rings():
    cent = int(dim/2)
    for size in range(510, -15, -25):
        x = y = cent - size
        x1 = y1 = cent + size
        c = all_colors[random.randint(0, len(all_colors) - 1)]
        active_c = all_colors[random.randint(0, len(all_colors) - 1)]
        canvas.create_oval(x, y, x1, y1, fill = c, activefill = active_c)
    
if __name__ == '__main__':
    window = tkinter.Tk()
    
    dim = 1000
    window.geometry('{0}x{0}'.format(dim))
    all_colors = [colour.Color(x).hex_l for x in colour.COLOR_NAME_TO_RGB]
    
    canvas = tkinter.Canvas(window, width=dim, height=dim, bg='black')
    canvas.pack()
    rings()
    window.mainloop()