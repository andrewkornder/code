from keyboard import Keyboard as kbA
from keyboard2 import Keyboard as kbB
from keyboard2 import Text
from ml.genetic_algorithm import Optimizer
from tkinter import Tk, Canvas


t = Text.wikipedia_text(2000)


class Graph:
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.oa, self.ob = Optimizer(a, t, minimize=True), Optimizer(b, t, minimize=True)

        self.w, self.h = 1500, 800
        self.x_padding, self.y_padding = self.w // 50, self.h // 50

        self.root = Tk()
        self.root.geometry(f'{self.w + 2 * self.x_padding}x{self.h + 2 * self.y_padding}+50+30')

        self.root.bind('<space>', self.toggle_state)
        self.root.bind('<q>', self.quit)
        self.root.bind('<r>', self.reset)

        self.canvas = Canvas(self.root, width=self.w + 2 * self.x_padding,
                             height=self.h + 2 * self.y_padding, bg='white')
        self.canvas.pack()

        self.y_scale = (0.8 * self.h) / 2000
        self.y_floor = 0

        self.line_width = 1

        self.draw_axes()
        self.ap = []
        self.bp = []

        self.running = False
        self.root.after(1, self.loop)
        self.root.mainloop()

    def loop(self):
        if not self.running:
            self.root.after(1, self.loop)
            return

        self.canvas.delete('to delete')
        self.oa.new_generation()
        self.add_round(self.ap, self.oa.scores[0], color='red')

        self.ob.new_generation()
        self.add_round(self.bp, self.ob.scores[0], color='blue')
        print(f'\r{self.oa.scores[0]:.4f}, {self.ob.scores[0]:.4f}', end='')
        self.root.after(1, self.loop)

    def toggle_state(self, _):
        self.running = not self.running

    def reset(self, _):
        self.oa.initiate()
        self.ob.initiate()

        self.ap = []
        self.bp = []

    def quit(self, _):
        self.root.destroy()
        print()
        print(score(self.oa.best), score(self.ob.best))

        print(self.oa.best.get_format())
        print(self.ob.best)

    def draw_axes(self):
        floor = self.h - self.y_padding
        self.canvas.create_line(self.x_padding, 0, self.x_padding, floor,
                                fill='black', width=self.line_width)
        self.canvas.create_line(self.x_padding, floor, self.w, floor,
                                fill='black', width=self.line_width)

    def calc_height(self, height):
        return self.h + self.y_scale * (self.y_floor - height) + self.y_padding

    def add_round(self, l, h, color='black'):  # maybe add worst score each round
        l.append(self.calc_height(h))

        x_scale = (self.w - self.x_padding) / len(l)
        x = self.x_padding
        last_y, last_x = l[0], self.x_padding
        for point in l:
            self.canvas.create_line(last_x, last_y, x, point, fill=color, width=self.line_width, tags=('to delete',))
            last_y, last_x = point, x
            x += x_scale


def score(kb):
    return kb.fitness_score(Text.wikipedia_text(1000))


if __name__ == '__main__':
    Graph(kbA, kbB)