# numbers guessing game for some kinda nn, draw into a tkinter window, then it shows confidence levels for various

from tkinter import Tk, Canvas
from math import exp


class Grid:
    def __init__(self, arr):
        self.s = 50
        self.array = arr
        self.w, self.h = len(arr[0]) * self.s, len(arr) * self.s
        self.r = Tk()
        self.r.geometry(f'{self.w}x{self.h}')

        self.canvas = Canvas(self.r, height=self.h, width=self.w, bg='black')

        self.canvas.pack()
        self.draw()

        self.r.mainloop()

    def draw(self):
        for r, row in enumerate(self.array):
            y = self.s * r
            for c, pix in enumerate(row):
                x = self.s * c
                self.canvas.create_rectangle(
                    x, y, x + self.s, y + self.s,
                    fill='#ffffff' if pix else '#000000')


class Drawing:
    def __init__(self, root, size, arr_size):
        self.scale_w, self.scale_h = [size[a] // arr_size[a] for a in range(2)]
        self.array = [[0] * arr_size[0] for i in range(arr_size[1])]

        self.w, self.h = size
        self.parent = root

        self.screen = Canvas(root, height=self.h, width=self.w, bg='black')
        self.screen.pack()

        self.mouse = Mouse(self)

        self.model = None  # TODO
        self.parent.bind('<p>', self.make_window)

        self.parent.mainloop()

    @staticmethod
    def sigmoid(x): return 1 / (exp(-x) + 1)

    def dist(self, i, j):
        # do nothing
        return

    def clear(self, e):
        self.array = [[0 for a in r] for r in self.array]
        self.screen.delete('all')

    def make_window(self, e):
        Grid(self.array)


class Mouse:
    def __init__(self, canvas):
        self.is_clicked = False
        self.loc = 0, 0
        self.parent = canvas
        self.screen = canvas.screen

        self.screen.bind('<Motion>', self.draw)
        self.screen.bind('<ButtonPress>', self.toggle)
        self.screen.bind('<ButtonRelease>', self.toggle)
        self.parent.parent.bind('<space>', self.parent.clear)

    def toggle(self, e): self.is_clicked = not self.is_clicked

    def draw(self, e):
        if e.x > self.parent.w or e.y > self.parent.h:
            return

        if not self.is_clicked:
            self.loc = e.x, e.y
            return

        self.screen.create_line(*self.loc, e.x, e.y, fill='white')
        self.loc = e.x, e.y

        i, j = e.y // self.parent.scale_h, e.x // self.parent.scale_w
        self.parent.array[i][j] = 1


if __name__ == '__main__':
    r = Tk()
    r.geometry('500x500+0+0')

    cv = Drawing(r, (500, 500), (20, 20))
