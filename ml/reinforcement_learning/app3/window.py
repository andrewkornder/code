from constants import *
from grid import Grid

from tkinter import Tk, Canvas, Button, Label, Scale, IntVar, StringVar
from random import sample, randint


class App:
    @classmethod
    def random(cls, size, walls, blocks, start, goal, **kwargs):
        s2 = size * size

        def random_adjacent(k):
            choices = []
            r, c = divmod(k, size)
            if r != 0:
                choices.append(k - size)
            if r != size - 1:
                choices.append(k + size)
            if c != 0:
                choices.append(k - 1)
            if c != size - 1:
                choices.append(k + 1)
            return choice(choices)

        if start is None:
            start = 0
        elif start is True:
            start = randint(0, s2 - 1)

        if goal is None:
            goal = s2 - 1
        elif goal is True:
            goal = randint(0, s2 - 1)

        unique = [i for i in range(s2) if i not in (start, goal)]
        return cls(size, start=start, goal=goal,
                   blocks=sample(unique, int(blocks * s2)),
                   walls=[(k, random_adjacent(k)) for k in sample(unique, int(walls * s2))], **kwargs)

    def __init__(self, size, start=None, goal=None, blocks=None, walls=None, training=0):
        self.size = size

        self.training = training
        self.root, self.grid, self.rounds, self.training_label = self.create_window(start, goal, walls, blocks)

        self.mouse_down = False
        self.mouse_start = None

        self.showing_numbers = False
        self.showing_moves = False

    def get_rounds(self):
        return 10 ** self.rounds.get()

    def run(self, auto=False):
        if auto:
            self.root.after(50, self.model)
        self.root.mainloop()

    def create_window(self, start, goal, walls, blocks):
        dim = Constants.size * self.size

        root = Tk()
        root.geometry(f'{dim + Constants.size}x{dim}')

        grid = Grid(self, Canvas(root), self.size, start, goal,
                    blocks if blocks else [], walls if walls else [], self.mouse_handler)

        root.bind('<Return>', lambda *_: self.model())
        root.bind('<KeyPress>', lambda e: self.key_handler(e.keysym, True))
        root.bind('<KeyRelease>', lambda e: self.key_handler(e.keysym, False))

        rounds = IntVar(root, Constants.default_rounds)
        training_label = StringVar(root, Constants.training_options[self.training])

        Label(root, text='rounds:').grid(row=1, column=1)
        Scale(root, from_=0, to=7, variable=rounds, length=Constants.size * 0.6,
              orient='horizontal').grid(row=2, column=1)

        Label(root, textvariable=training_label).grid(row=3, column=1)
        Button(root, text='run', command=lambda: self.model()).grid(row=4, column=1)

        return root, grid, rounds, training_label

    def change_training(self, increment):
        self.training += increment
        if self.training == len(Constants.training_options):
            self.training = 0
        elif self.training < 0:
            self.training = len(Constants.training_options) - 1

        self.training_label.set(Constants.training_options[self.training].replace('_', ' '))

    def mouse_handler(self, button, boolean, x, y):
        if button != -1:  # -1 is for motion
            pos = flatten(self.size, y // Constants.size, x // Constants.size)

            if button == 1:
                if boolean:
                    self.mouse_start = pos
                elif pos == self.mouse_start:
                    self.grid.create_block(pos)
                else:
                    self.grid.create_wall(pos, self.mouse_start)
            elif button == 3:
                if boolean:
                    self.grid.iterate_pos(pos)

        else:  # handle mouse movement
            self.grid.reset_drawings()

    def key_handler(self, key, boolean):
        if key == 'space':
            self.showing_numbers = boolean
            self.grid.draw_nums() if boolean and self.showing_numbers else self.grid.delete('numbers')
            return

        if key == 'm':
            self.showing_moves = boolean
            self.grid.show_moves() if boolean else self.grid.delete('moves')
            return

        if boolean:
            if key == 'Left':
                self.change_training(-1)
                return
            if key == 'Right':
                self.change_training(1)
                return
            if key == 'Escape':
                self.grid.delete('path')
                return
            if key == 'BackSpace':
                self.grid.reset_obstacles()
                return
            if key == 'minus':
                self.grid.change_size(self.size - 1, align=1)
                return
            if key == 'equal':
                self.grid.change_size(self.size + 1, align=1)
                return
            if key in '123457689':
                self.grid.change_size(int(key))
                return

            print(f'{key} is not bound to any action')

    def model(self):
        pass
