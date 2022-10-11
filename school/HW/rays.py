import tkinter
import math

def rays():
    center = (500, 500)
    center_full = [(x, y) for x in range(0, 1000) for y in range(0, 1000) if 301 > math.dist((x, y), center) > 300]

    for i, xy in enumerate(center_full):
        num = i % 8
        if num == 0:
            canvas.create_line(xy, center, fill = 'white')
        else:
            x, y = xy
            if x < 500:
                if y < 500:
                    to = (0, 0)
                else:
                    to = (0, 1000)
            else:
                if y < 500:
                    to = (1000, 0)
                else:
                    to = (1000, 1000)
            canvas.create_line(xy, to, fill = 'white')


if __name__ == '__main__':
    window = tkinter.Tk()
    dim = 1000
    window.geometry('{0}x{0}'.format(dim))
    canvas = tkinter.Canvas(window, width=dim, height=dim, bg='black')
    canvas.pack()
    rays()
    window.mainloop()