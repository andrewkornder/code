from constants import *
from snake_grid import SnakeGrid, SnakeModel

from tkinter import Tk, Canvas, Button, Label, Scale, IntVar, StringVar


Constants.goal_color = 'red'
Constants.start_color = 'orange'


class SnakeApp:
    def __init__(self, size, start=None, blocks=(), walls=(), apples=(), training=0):
        self.keys = {
            'a': lambda: self.grid.apple.next(),
            'Left': lambda: self.change_training(-1),
            'Right': lambda: self.change_training(1),
            'Escape': lambda: self.grid.delete('path'),
            'BackSpace': lambda: self.grid.reset_obstacles(),
            'minus': lambda: self.grid.change_size(self.size - 1, align=1),
            'equal': lambda: self.grid.change_size(self.size + 1, align=1),
            **{str(i): lambda s=i: self.grid.change_size(s) for i in range(1, 10)}
        }

        self.size = size

        self.training = training
        self.root, self.grid, self.rounds, self.training_label = self.create_window(start, apples, walls, blocks)

        self.mouse_down = False
        self.mouse_start = None

    def get_rounds(self):
        return 10 ** self.rounds.get()

    def run(self, auto=False):
        if auto:
            self.root.after(50, self.model)
        self.root.mainloop()

    def create_window(self, start, apples, walls, blocks):
        dim = Constants.size * self.size

        root = Tk()
        root.geometry(f'{dim + Constants.size}x{dim}')

        grid = SnakeGrid(self, Canvas(root), self.size, start, blocks, walls, self.mouse_handler,
                         apples)

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
                    self.grid.set_start(pos)

        else:  # handle mouse movement
            self.grid.reset_drawings()

    def key_handler(self, key, boolean):
        if key == 'space':
            self.grid.showing_numbers = boolean
            self.grid.draw_nums() if boolean and self.grid.showing_numbers else self.grid.delete('numbers')
            return

        if key == 'm':
            self.grid.showing_moves = boolean
            self.grid.show_moves() if boolean else self.grid.delete('moves')
            return

        if boolean:
            if key in self.keys:
                self.keys[key]()
            print(f'{key} is not bound to any action')
            return

    def model(self):
        if None in (self.grid.apple, self.grid.start):
            return

        rounds = self.get_rounds()
        model = SnakeModel.from_grid(self.grid, self.grid.reward,
                                     training_type=Constants.training_options[self.training]).train(rounds)
        path = model.play_game()

        if path[-1] == -1:
            print('failed to find path')
            return

        self.draw_path(path)

    def draw_path(self, path):
        def draw_step():
            canvas.delete('walk')

            step = path.pop()
            x, y = list(map(lambda i: i * Constants.size, divmod(step, self.size)))
            canvas.create_rectangle(x, y, x + Constants.size, y + Constants.size,
                                    fill=Constants.walk_color, tags=('walk',))

            if path:
                canvas.after(ms, draw_step())

        path = path[::-1]
        canvas = self.grid.canvas
        ms = Constants.walk_time / len(path)

        draw_step()


if __name__ == '__main__':
    app = SnakeApp(5, start=0)
    app.run()
