import tkinter
import math
from colour import Color

def loading():
    global xys, canvas, window
    size = 40
    for i, (x, y) in enumerate(xys):
        canvas.create_oval(x - size, y - size, x + size, y + size, fill=all_colors[i])
    xys = xys[1:] + [xys[0]]
    window.after(100, loading)

def main():
    global canvas, window
    window = tkinter.Tk()
    dim = 1000
    window.geometry('{0}x{0}'.format(dim))

    global all_colors, xys
    all_colors = ['#000000']*3 + list([x.hex_l for x in Color('black').range_to(Color('white'), 17)])
    xy_list = [(x, y) for x in range(200, 802) for y in range(200, 802) if math.dist((x, y), (500, 500)) == 300]
    xys = xy_list[:2]

    i, inc = 1, 2
    while len(xys) != len(xy_list):
        if i == 19:
            i -= 1
            inc = -2
        else:
            i += inc
        xys.append(xy_list[i])

    canvas = tkinter.Canvas(window, width=dim, height=dim, bg='black')
    canvas.pack()
    loading()
    window.mainloop()

if __name__ == '__main__':
    main()