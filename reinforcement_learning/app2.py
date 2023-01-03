from random import choice, sample, randint
import numpy as np
from tkinter import Tk, Canvas
from math import log10
from time import perf_counter
import scipy.interpolate as si

SIZE = 100
GOAL = 9

WALL_WIDTH = 1

BG = 'white'
BLOCK_COLOR = '#333333'
WALL_COLOR = '#333333'
GOAL_COLOR = 'green'
START_COLOR = 'red'
GRID_COLOR = ''
WALK_COLOR = 'blue'


class Legality:
    def adjacent(self, k):
        r, c = k // self.row, k % self.row
        if r != 0:
            yield k - self.row
        if r != self.row - 1:
            yield k + self.row
        if c != 0:
            yield k - 1
        if c != self.row - 1:
            yield k + 1
        yield k

    def legal(self, state, action):
        if action == state:
            return True

        if action in self.blocks:
            return False

        if (state, action) in self.walls or (action, state) in self.walls:
            return False

        if not (0 <= action < self.size):
            return False

        if abs(state - action) == 1:
            return state // self.row == action // self.row
        else:
            return state % self.row == action % self.row

    def __getitem__(self, item):
        return self.arr[item]

    def __setitem__(self, key, value):
        self.arr[key] = value

    def __init__(self, size, goal, walls, blocks):
        self.row = size
        self.size = size * size

        self.walls, self.blocks = walls, blocks
        self.goal = goal

        self.arr = []
        for i in range(self.size):
            self.arr.append([int(self.legal(i, k)) for k in range(self.size)])

        self.arr = np.array(self.arr)
        if goal is not None:
            self[goal, goal] = GOAL

    def moves(self, i):
        return [k for k in self.adjacent(i) if self.legal(i, k)]

    def moves_2d(self, r, c):
        i = r * self.row + c
        return [k for k in self.adjacent(i) if self.legal(i, k)]

    def change_goal(self, goal):
        if self.goal:
            self[self.goal, self.goal] = 1

        self[goal, goal] = GOAL
        self.goal = goal


class App2:
    @staticmethod
    def grid_bounding(r, c):
        c, r = c * SIZE, r * SIZE
        return [(c + SIZE * a, r + SIZE * b) for a in (0, 1) for b in (0, 1)]

    @staticmethod
    def scale_down(e):
        return e.y // SIZE, e.x // SIZE

    def grid_bounding_flat(self, i):
        r, c = map(lambda x: x * SIZE, self.expand(i))
        return [(c + SIZE * a, r + SIZE * b) for a in (0, 1) for b in (0, 1)]

    def flatten(self, *p):
        return (lambda r, c: self.size * r + c)(*(p if len(p) > 1 else p[0]))

    def expand(self, k):
        return k // self.size, k % self.size

    @classmethod
    def random_start(cls, size, blocks=0.2, walls=0.2, start=None, goal=None, **kwargs):
        s2 = size * size

        def random_adjacent(k):
            choices = []
            r, c = k // size, k % size
            if r != 0:
                choices.append(-size)
            if r != size - 1:
                choices.append(size)
            if c != 0:
                choices.append(-1)
            if c != size - 1:
                choices.append(1)
            return k + choice(choices)

        if start is None:
            start = 0
        elif start is True:
            start = randint(0, s2 - 1)

        if goal is None:
            goal = s2 - 1
        elif goal is True:
            goal = randint(0, s2 - 1)

        unique = [i for i in range(s2) if i not in (start, goal)]

        blocks = sample(unique, int(blocks * s2))
        walls = [(k, random_adjacent(k)) for k in sample(unique, int(walls * s2))]

        return cls(size, start=start, goal=goal, blocks=blocks, walls=walls, **kwargs)

    def __init__(self, size, start=None, goal=None, blocks=None, walls=None,
                 rounds=1000, decay=0.75, step=1):
        self.size = size
        self.s2 = size * size

        self.rounds = rounds
        self.decay = decay
        self.step = step

        # creating window
        self.dim = size * SIZE

        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.dim, height=self.dim)

        self.root.geometry('{0}x{0}'.format(self.dim))
        self.canvas.pack()

        self.mouse_down = False
        self.mouse_start = None
        self.canvas.bind('<Button-3>', lambda e: self.iterate_pos(self.flatten(self.scale_down(e))))
        self.canvas.bind('<ButtonPress-1>', lambda e: self.toggle_press(*self.scale_down(e)))
        self.canvas.bind('<ButtonRelease-1>', lambda e: self.toggle_press(*self.scale_down(e)))
        self.canvas.bind('<Motion>', lambda e: self.reset_drawings())

        self.root.bind('<Return>', lambda *_: self.model())
        self.root.bind('<BackSpace>', lambda *_: self.canvas.delete('path', 'Walker'))

        self.showing_numbers = False
        self.root.bind('<KeyPress>', lambda e: self.key_handler(e.keysym, True))
        self.root.bind('<KeyRelease>', lambda e: self.key_handler(e.keysym, False))

        self.showing_moves = False

        self.start = start
        self.goal = goal

        self.walls = [] if walls is None else walls
        self.blocks = [] if blocks is None else blocks

        self.legality = Legality(size, goal=goal, walls=self.walls, blocks=self.blocks)

    def reset_drawings(self):
        if self.showing_moves:
            self.canvas.delete('moves')
            self.show_moves()

    def key_handler(self, key, boolean):
        if key == 'space':
            self.showing_numbers = boolean
            self.draw_nums() if boolean and self.showing_numbers else self.canvas.delete('numbers')

        elif key == 'm':
            self.showing_moves = boolean
            if boolean:
                self.show_moves()
            else:
                self.canvas.delete('moves')

    def show_moves(self):
        r, c = (max(0, self.root.winfo_pointery() - self.root.winfo_rooty()) // SIZE,
                max(0, self.root.winfo_pointerx() - self.root.winfo_rootx()) // SIZE)
        for j in self.legality.moves_2d(r, c):
            r1, c1 = self.expand(j)
            self.canvas.create_rectangle(c1 * SIZE, r1 * SIZE, c1 * SIZE + SIZE, r1 * SIZE + SIZE,
                                         fill='blue', tags=('moves',))

    def run(self, auto):
        self.root.after(10, self.draw_grid)
        if auto and None not in (self.start, self.goal):
            self.root.after(50, self.model)
        self.root.mainloop()

    def draw_nums(self):
        for r in range(self.size):
            for c in range(self.size):
                i = r * self.size + c
                self.canvas.create_text((c + 0.5) * SIZE, (r + 0.5) * SIZE, text=str(i),
                                        font=('Arial', 20), fill='#444444', tags=('numbers', str(i)))

    def draw_grid(self):
        for pos in range(self.s2):
            if pos in self.blocks:
                color = BLOCK_COLOR
            elif pos == self.goal:
                color = GOAL_COLOR
            elif pos == self.start:
                color = START_COLOR
            else:
                color = BG

            x0, y0 = pos % self.size * SIZE, pos // self.size * SIZE
            self.canvas.create_rectangle(x0, y0, x0 + SIZE, y0 + SIZE,
                                         fill=color, width=WALL_WIDTH, tags=('rc_%s' % pos,), outline=GRID_COLOR)

        for a, b in self.walls:
            a_p, b_p = self.grid_bounding_flat(a), self.grid_bounding_flat(b)
            self.canvas.create_line(*(lambda x, y: x + y)(*tuple(set(a_p).intersection(b_p))),
                                    fill=WALL_COLOR, width=WALL_WIDTH, tags=(f'wall_{a}x{b}', f'wall_{b}x{a}'))

    def toggle_press(self, r, c):
        self.mouse_down = not self.mouse_down

        if self.mouse_down:
            self.mouse_start = r, c
        elif (r, c) == self.mouse_start:
            self.set_block(self.flatten(r, c))
        else:
            self.set_wall(self.flatten(self.mouse_start), self.flatten(r, c))

    def set_block(self, i):
        if i in (self.goal, self.start):
            return

        if i in self.legality.blocks:
            self.canvas.itemconfigure('rc_%s' % i, fill=BG)
            self.legality.blocks.remove(i)
            return

        self.canvas.itemconfigure(f'rc_%s' % i, fill=BLOCK_COLOR)
        self.legality.blocks.append(i)

    def iterate_pos(self, p):  # null -> start -> goal -> null
        if p in self.blocks:
            return

        color = START_COLOR
        if self.goal is None and p == self.start:
            self.start, self.goal, color = None, p, GOAL_COLOR
            self.legality.change_goal(p)
        elif p == self.goal:
            self.goal, color = None, BG
        elif self.start is None:
            self.start = p
        else:
            print('cannot have more than 1 start position at any given time')
            return

        self.canvas.itemconfigure('rc_%s' % p, fill=color)

    def set_wall(self, a, b):
        if (a, b) in self.legality.walls:
            self.legality.walls.remove((a, b))
            self.canvas.delete(f'wall_{a}x{b}')
            return
        elif (b, a) in self.legality.walls:
            self.legality.walls.remove((b, a))
            self.canvas.delete(f'wall_{b}x{a}')
            return

        self.legality.walls.append((a, b))

        a_p, b_p = self.grid_bounding_flat(a), self.grid_bounding_flat(b)
        intersection = tuple(set(a_p).intersection(b_p))

        if len(intersection) != 2:
            print(f'{a} and {b} were not adjacent')
            return

        p0, p1 = intersection
        self.canvas.create_line(*p0, *p1, fill=WALL_COLOR, width=WALL_WIDTH, tags=f'wall_{a}x{b}')

    def model(self):
        Q = np.zeros([self.s2, self.s2])
        states = [i for i in range(self.s2) if i not in self.blocks]

        l = int(log10(self.rounds)) + 1
        for rnd in range(self.rounds):
            if rnd % 100 == 99:
                print(f'\r{rnd + 1:>{l}} / {self.rounds}', end='')

            state = choice(states)
            action = choice(self.legality.moves(state))

            Q[state, action] += self.step * (self.legality[state, action] +
                                             self.decay * Q[action, np.argmax(Q[action])] - Q[state, action])

        print('\nfinished training')

        state, path = self.start, [self.start]
        for _ in range(self.s2):
            state = np.argmax(Q[state,])
            path.append(state)
            if state == self.goal:  # goal
                break
        else:
            print('path not found', path)
            return

        self.path_display(path)

    def path_display(self, path):
        self.canvas.delete('path')

        points = [(lambda b: [sum(c) / 4 for c in b])(zip(*self.grid_bounding(*self.expand(point)))) for point in path]
        for i, point in enumerate(points[1:]):
            self.canvas.create_line(*points[i], *points[i + 1], fill='blue', width=3, tags='path')

        Walk(self.canvas, points, time=3, radius=5)


class Walk:
    def __init__(self, canvas, points, time, radius):
        self.points = np.asarray([np.array(point) for point in points])

        self.length = len(points)
        self.canvas = canvas
        self.total_time = time

        self.start = perf_counter()
        self.last = points[0]
        self.radius = radius
        self.drawing = canvas.create_oval(*(lambda x, y, r: (x - r, y - r, x + r, y + r))(*points[0], radius),
                                          fill=WALK_COLOR, tags=('Walker',))

        self.N = 200

        turns, sign = 0, [False, False]
        for i, point in enumerate(self.points[1:]):
            new_sign = [a >= 0 for a in self.points[i] - point]
            if new_sign != sign:
                turns += 1
            sign = new_sign
        self.path = self.bspline(degree=turns)  # more turns, the higher the degree

        self.draw_point()

    def bspline(self, degree=3, periodic=False):
        return (lambda cv: (lambda degree, count: (
            lambda kv: np.array(si.splev(np.linspace(periodic, (count - degree), self.N), (kv, cv.T, degree))).T)(
            np.arange(0 - degree, count + degree + degree - 1, dtype='int') if periodic else np.concatenate(
                ([0] * degree, np.arange(count - degree + 1), [count - degree] * degree))))(
            np.clip(degree, 1, degree if periodic else self.length - 1), len(cv)))(
            (lambda factor, fraction: np.concatenate((self.points,) * factor + (self.points[:fraction],)))(
                *divmod(self.length + degree + 1, self.length)) if periodic else self.points[:])

    def draw_point(self):
        t = min(1, (perf_counter() - self.start) / self.total_time)
        x, y = self.path[int((self.N - 1) * t)]

        self.canvas.moveto(self.drawing, x - self.radius, y - self.radius)
        self.canvas.create_line(*self.last, x, y, fill=WALK_COLOR, tags=('Walker',))
        self.last = x, y
        if t < self.total_time:
            self.canvas.after(1, self.draw_point)
        else:
            self.canvas.delete('Walker')


if __name__ == '__main__':
    App2(5).run(False)
