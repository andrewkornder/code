import numpy as np
from random import choice, sample, randint
from tkinter import Tk, Canvas, StringVar, Button, Entry, Label
from time import perf_counter
from scipy.interpolate import BSpline


SIZE = 100
GOAL = 100
DEFAULT_ROUNDS = 2

WALK_COLOR = 'blue'
WALK_TIME = 3

WALL_WIDTH = 1

BG = 'white'
BLOCK_COLOR = '#333333'
WALL_COLOR = BLOCK_COLOR
GOAL_COLOR = 'green'
START_COLOR = 'red'
GRID_COLOR = ''


class App:
    def flatten(self, r, c):
        return r * self.size + c

    def expand(self, k):
        return divmod(k, self.size)

    def bounding(self, *args):
        r, c = self.expand(args[0]) if len(args) == 1 else args
        return [((c + a) * SIZE, (r + b) * SIZE) for a in range(2) for b in range(2)]

    def intersection(self, a, b):
        return set(self.bounding(a)).intersection(self.bounding(b))

    def adjacent(self, k):
        r, c = divmod(k, self.size)
        if r != 0:
            yield k - self.size
        if r != self.size - 1:
            yield k + self.size
        if c != 0:
            yield k - 1
        if c != self.size - 1:
            yield k + 1
            
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

    def __init__(self, size, start=None, goal=None, blocks=None, walls=None, model=None, record=0):
        self.size = size
        self.flat_size = size * size

        self.start, self.goal = start, goal
        self.blocks, self.walls = blocks if blocks else [], walls if walls else []

        self.root, self.canvas, self.entry = self.create_window()
        self.mouse_down = False
        self.mouse_start = None

        self.showing_numbers = False
        self.showing_moves = False

        self.model = (lambda: model(self)) if model is not None else (lambda *args: None)
        self.record_interval = record

    def run(self, auto=False):
        if auto:
            self.root.after(50, self.model)
        self.root.mainloop()

    def create_window(self):
        dim = SIZE * self.size

        root = Tk()
        root.geometry(f'{dim + SIZE}x{dim}')

        root.bind('<Return>', lambda *_: self.model())
        root.bind('<BackSpace>', lambda *_: self.canvas.delete('path'))

        canvas = Canvas(root, width=dim, height=dim, background=BG)
        canvas.grid(row=0, column=0, rowspan=5)

        root.bind('<KeyPress>', lambda e: self.key_handler(e.keysym, True))
        root.bind('<KeyRelease>', lambda e: self.key_handler(e.keysym, False))

        canvas.bind('<ButtonPress>', lambda e: self.mouse_handler(e.num, True, e.x, e.y))
        canvas.bind('<ButtonRelease>', lambda e: self.mouse_handler(e.num, False, e.x, e.y))
        canvas.bind('<Motion>', lambda e: self.reset_drawings())

        pos = y = 0
        for _ in range(self.size):
            y1, x = y + SIZE, 0
            for _ in range(self.size):
                color = BG
                if pos in self.blocks:
                    color = BLOCK_COLOR
                elif pos == self.start:
                    color = START_COLOR
                elif pos == self.goal:
                    color = GOAL_COLOR

                x1 = x + SIZE
                canvas.create_rectangle(x, y, x1, y1,
                                        fill=color, outline=GRID_COLOR, tags=(f'loc_{pos}',))
                x = x1
                pos += 1
            y = y1

        for a, b in self.walls:
            inter = self.intersection(a, b)
            if len(inter) != 2:
                print(f'{a} and {b} were not adjacent')
                continue
            a_p, b_p = inter
            canvas.create_line(*a_p, *b_p, fill=WALL_COLOR, width=WALL_WIDTH,
                               tags=(f'wall_{a}x{b}', f'wall_{b}x{a}'))

        entry = StringVar(root, str(DEFAULT_ROUNDS))

        Label(root, text='rounds:').grid(row=1, column=1)
        Entry(root, textvariable=entry).grid(row=2, column=1)
        Button(root, text='run', command=lambda: self.model()).grid(row=3, column=1)

        return root, canvas, entry

    def mouse_handler(self, button, boolean, x, y):
        pos = self.flatten(y // SIZE, x // SIZE)
        if button == 1:
            if boolean:
                self.mouse_start = pos
            elif pos == self.mouse_start:
                self.create_block(pos)
            else:
                self.create_wall(pos, self.mouse_start)
        elif button == 3:
            if boolean:
                self.iterate_pos(pos)

    def key_handler(self, key, boolean):
        if key == 'space':
            self.showing_numbers = boolean
            self.draw_nums() if boolean and self.showing_numbers else self.canvas.delete('numbers')

        elif key == 'm':
            self.showing_moves = boolean
            self.show_moves() if boolean else self.canvas.delete('moves')

    def get_moves(self, r, c):
        k = self.flatten(r, c)
        for move in list(self.adjacent(k)):
            if move in self.blocks:
                continue
            if (k, move) in self.walls or (move, k) in self.walls:
                continue
            yield move
        yield k
        
    def draw_nums(self):
        for r in range(self.size):
            for c in range(self.size):
                self.canvas.create_text((c + 0.5) * SIZE, (r + 0.5) * SIZE, text=str(r * self.size + c),
                                        font=('Arial', 20), fill='#444444', tags=('numbers',))

    def show_moves(self):
        r, c = (max(0, self.root.winfo_pointery() - self.root.winfo_rooty()) // SIZE,
                max(0, self.root.winfo_pointerx() - self.root.winfo_rootx()) // SIZE)
        for j in self.get_moves(r, c):
            r1, c1 = self.expand(j)
            self.canvas.create_rectangle(c1 * SIZE, r1 * SIZE, c1 * SIZE + SIZE, r1 * SIZE + SIZE,
                                         fill='blue', tags=('moves',))

    def reset_drawings(self):
        if self.showing_moves:
            self.canvas.delete('moves')
            self.show_moves()
            
    def change_color(self, k, color):
        self.canvas.itemconfigure(f'loc_{k}', fill=color)
        
    def iterate_pos(self, k):
        if k in self.blocks:
            return
        
        if k == self.start:
            if self.goal is not None:
                self.change_color(self.goal, BG)
            self.start, self.goal, color = None, self.start, GOAL_COLOR
        elif k == self.goal:
            self.goal, color = None, BG
        else:
            if self.start is not None:
                self.change_color(self.start, BG)
            self.start, color = k, START_COLOR
        self.change_color(k, color)
        
    def create_block(self, k):
        if k in (self.start, self.goal):
            return
        
        if k in self.blocks:
            self.blocks.remove(k)
            self.change_color(k, BG)
            return
    
        self.change_color(k, BLOCK_COLOR)
        self.blocks.append(k)
        
    def create_wall(self, a, b):
        if (a, b) in self.walls:
            self.walls.remove((a, b))
            self.canvas.delete(f'wall_{a}x{b}')
            return
        elif (b, a) in self.walls:
            self.walls.remove((b, a))
            self.canvas.delete(f'wall_{b}x{a}')
            return

        inter = self.intersection(a, b)
        
        if len(inter) != 2:
            print(f'{a} and {b} were not adjacent')
            return
        
        a_p, b_p = inter
        self.canvas.create_line(*a_p, *b_p, fill=WALL_COLOR, width=WALL_WIDTH,
                                tags=(f'wall_{a}x{b}', f'wall_{b}x{a}'))
        self.walls.append((a, b))

    def get_legality_matrix(self):
        arr = []
        for state in range(self.flat_size):
            moves = list(self.adjacent(state)) + [state]
            arr.append([int(i in moves) for i in range(self.flat_size)])

        arr = np.array(arr)
        arr[:, self.goal] = GOAL

        for a, b in self.walls:
            arr[a, b] = 0
            arr[b, a] = 0

        for block in self.blocks:
            arr[block] = 0
            arr[:, block] = 0

        return arr


class PathDisplay:
    @staticmethod
    def circle(x, y, r):
        return x - r, y - r, x + r, y + r

    def __init__(self, points, canvas, style='linear', definition=100, radius=0.05):
        self.points = points if style == 'linear' else (self.b_spline(points, definition)
                                                        if style == 'interpolated' else [])
        self.length = len(self.points)
        self.canvas = canvas

        self.last = self.points[0]
        self.radius = int(radius * SIZE)

        self.ms = int(1000 * (WALK_TIME / self.length) - 1)
        self.start = perf_counter()
        self.drawing = canvas.create_oval(*self.circle(*self.last, self.radius), fill=WALK_COLOR, tags=('path',))
        self.iterate()

    @staticmethod
    def b_spline(points, n):
        degree, sign = 0, [False, False]
        for i, point in enumerate(points[1:]):
            new_sign = [a >= 0 for a in points[i] - point]
            if new_sign != sign:
                degree += 1
            sign = new_sign

        count = points.shape[0]

        degree = np.clip(degree, 1, count - 1)
        kv = np.clip(np.arange(count + degree + 1) - degree, 0, count - degree)

        return BSpline(kv, points, degree)(np.linspace(0, count - degree, n))

    def iterate(self):
        t = (perf_counter() - self.start) / WALK_TIME
        if t >= 1:
            return

        x, y = self.points[int(self.length * t)]
        self.canvas.create_line(*self.last, x, y, fill=WALK_COLOR, tags=('path',))
        self.canvas.moveto(self.drawing, x - self.radius, y - self.radius)
        self.last = x, y

        self.canvas.after(self.ms, self.iterate)


if __name__ == '__main__':
    TRAINING_TYPE = 2
    App(3).run()
    