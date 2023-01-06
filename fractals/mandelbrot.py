from PIL import ImageTk
from tkinter import Tk, Canvas
from time import time

<<<<<<< Updated upstream:fractals/mandelbrot.py

def mandelbrot(z, c):
    a, b = z
    x0, y0 = c
    return a * a - b * b + x0, 2 * a * b + y0


def magnitude(z):
    a, b = z
    return a * a + b * b

=======
>>>>>>> Stashed changes:mandelbrot.py

def iterate(c, threshold, rounds):
    z = c
    for _ in range(rounds):
        z = z * z + c
        if z.real > threshold:
            return 0

    return max(0, threshold * threshold - (z * z.conjugate()).real)


def draw_set(width, height, x0, x1, y0, y1, threshold, rounds):
    def sur(string):
        return '{%s}' % string
    ws, hs, cs = (x1 - x0) / width, (y1 - y0) / height, 255 / (threshold * threshold)

    root = Tk()
    root.geometry(f'{width}x{height}')

    canvas = Canvas(root, width=width, height=height, bg='black')
    canvas.pack()

    data = []

    for x in range(width):
        x_i = x0 + x * ws
        data.append(' '.join(f'#0000{int(cs * iterate(complex(x_i, y0 - y * hs), threshold, rounds)):02x}' for y in range(height)))
        print(f'\r{x_i - x0:>10.2f} / {x1 - x0}', end='')

    canvas.create_image(0, 0, image=ImageTk.PhotoImage(data=' '.join(map(sur, data))), anchor='nw')
    canvas.update()
    root.mainloop()


if __name__ == '__main__':
    draw_set(1920, 1080, -3, 3, -1.7, 1.7, 2, 256)
