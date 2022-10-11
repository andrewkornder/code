from threading import Thread
from time import sleep
from math import isqrt
from tkinter import Tk, Canvas
from random import choice
from itertools import chain


THREADING = True


class Optimizer:
    default_population, default_p_size = 120, 15

    @staticmethod
    def get_p_size(population_size):
        return int(-0.5 + isqrt(1 + 8 * population_size) / 2)

    @staticmethod
    def get_population_size(p_size):
        return int(0.5 * p_size * (p_size - 1))

    def define_sizes(self, population_size, p_size):
        if population_size is None and p_size is None:
            return self.default_population, self.default_p_size

        elif population_size is None:
            return self.get_population_size(p_size), p_size

        elif p_size is None:
            return population_size, self.get_p_size(population_size)
        return population_size, p_size

    def __init__(self, cls, training_material, population_size=None, p_size=None,
                 minimize=False, full_refresh=True, children_proportion=0.1):  # children_proportion can't be >= 0.5
        if full_refresh:
            self.population_size, self.p_size = self.define_sizes(population_size, p_size)
        else:
            self.population_size = self.default_population if population_size is None else population_size
            self.p_size = int(children_proportion * self.population_size) if p_size is None else p_size
        self.minimize = minimize

        self.object = cls
        self.training_material = training_material
        self.generation = [cls.randomize() for _ in range(self.population_size)]
        self.next_round = self.new_generation if full_refresh else self.add_children

        # quality of life things
        self.round = 0
        self.record = RecordHolder(None, None, None, minimize=minimize)
        self.scores, self.average, self.worst = [], 0, 0

    @property
    def snapshot(self):
        return self.scores[-1], self.average, self.worst

    @property
    def best(self):
        return self.record.obj

    def initiate(self):
        self.__init__(self.object, self.training_material, self.population_size, self.p_size, self.minimize,
                      full_refresh=(self.next_round == self.new_generation))

    def new_generation(self):
        self.round += 1

        self.scores, survivors = self.get_scores()
        survivors = survivors[-self.p_size:]
        self.generation = []
        for i, a in enumerate(survivors):
            self.generation.extend(self.object.merge(a, b) for b in survivors[i:])

    def add_children(self):
        self.round += 1

        self.scores, self.generation = self.get_scores()
        self.generation = list(self.generation[self.p_size:])
        top = self.generation[-2 * self.p_size:]

        for _ in range(self.p_size):
            self.generation.append(self.object.merge(choice(top), choice(top)))

    def get_scores(self):
        def thread_score(to_score):
            score = to_score.fitness_score(self.training_material)
            scores.append((score, to_score))

        scores = []
        threads = []
        for obj in self.generation:
            thread = Thread(target=thread_score, args=(obj,))
            thread.start()
            threads.append(thread)

        while any(t.is_alive() for t in threads):
            sleep(0.1)

        sorted_scores = sorted(scores, reverse=self.minimize,  key=lambda x: x[0])
        scores, objs = list(zip(*sorted_scores))

        self.worst, self.average = scores[0], sum(scores) / self.population_size
        self.record.compare(*sorted_scores[-1], self.round)
        return scores, objs

    def output(self):
        scores = ", ".join(map(lambda x: f'{x:.3f}', self.scores[:-4:-1]))
        return f'{self.round} | scores: {scores} | average: {self.average:.3f} | worst: {self.worst:.3f}'

    def run(self, rounds):
        for i in range(rounds):
            self.next_round()
            print(f'\r{self.output()}', end=' ' * 10)

        print(f'\nbest score:{self.record.score}')
        return self.record.obj


class Graph:
    def __init__(self, cls, training_material, floor=0, scale=0.8, size=1000, comparisons=None,
                 minimize=False, text_output=False, full_refresh=True):
        self.training_material = training_material
        self.object = cls

        self.optimizer = Optimizer(cls, training_material, minimize=minimize, full_refresh=full_refresh)
        self.w, self.h = 1500, 800
        self.x_padding, self.y_padding = self.w // 50, self.h // 50

        self.root = Tk()
        self.root.geometry(f'{self.w + 2 * self.x_padding}x{self.h + 2 * self.y_padding}+0+0')

        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        self.root.bind('<space>', self.toggle_state)
        self.root.bind('<q>', self.quit)
        self.root.bind('<r>', self.reset)
        self.root.bind('<s>', self.rescale)

        self.canvas = Canvas(self.root, width=self.w + 2 * self.x_padding,
                             height=self.h + 2 * self.y_padding, bg='white')
        self.canvas.pack()

        self.user_pref = scale, size, floor
        self.y_scale = scale * self.h / size
        self.y_floor = floor if floor else (0.15 * size)

        self.line_width = 5
        self.font = ('Niagara Bold', 15)

        self.comparisons = comparisons
        if comparisons:
            self.add_comparisons(comparisons)
        self.draw_axes()

        self.points = []
        self.text_output = text_output

        if self.text_output:
            print(f'{"ROUND":^15}|{"BEST":^15}|{"AVERAGE":>15}')

        self.running = False
        self.root.after(1, self.loop)

    def loop(self):
        if not self.running:
            self.root.after(1, self.loop)
            return

        self.optimizer.next_round()
        self.add_round(*self.optimizer.snapshot)
        if self.text_output:
            print(f'\r{self.optimizer.round:^15}|{self.optimizer.scores[-1]:^15.3f}|{self.optimizer.average:>15.3f}',
                  end='')

        self.root.after(1, self.loop)

    def toggle_state(self, _):
        self.running = not self.running

    def reset(self, *_):
        self.optimizer.initiate()
        self.points = []

        scale, size, floor = self.user_pref
        self.y_scale = (scale * self.h) / size
        self.y_floor = floor if floor else (0.15 * size)
        self.line_width = 5

        self.canvas.delete('comparisons')
        self.add_comparisons(self.comparisons)

    def quit(self, *_):
        self.root.destroy()
        if self.text_output:
            print()
        print(self.optimizer.best)

    def run(self):
        self.root.mainloop()
        return self.optimizer.best

    def calc_height(self, height):
        return self.h + self.y_scale * (self.y_floor - height) + self.y_padding

    def undo_calc(self, x):
        return (self.h + self.y_padding - x) / self.y_scale + self.y_floor

    def add_comparisons(self, comparisons):
        for h in comparisons:
            y = self.calc_height(h)
            self.canvas.create_line(self.x_padding, y, self.w, y, fill='grey', dash=[5, 1], tags=('comparisons',))

    def rescale(self, *_, s=0.8):
        if not self.points:
            return

        self.points = [[self.undo_calc(entry) for entry in point] for point in self.points]
        all_points = list(chain.from_iterable(self.points))
        self.y_floor = min(all_points) * s
        self.y_scale = self.h / (max(all_points) - self.y_floor)

        self.canvas.delete('comparisons')
        self.add_comparisons(self.comparisons)

        self.points = [[self.calc_height(entry) for entry in point] for point in self.points]
        self.add_round()

    def draw_points(self, x0, x1, *args):
        for y0, y1, color in zip(*args):
            if y1 >= self.h - self.y_padding or y1 <= 0:
                self.rescale()
                return
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=self.line_width, tags=('to delete',))

    def add_round(self, *args, colors=('blue', 'red', 'green')):  # maybe add worst score each round
        self.canvas.delete('to delete')
        if args:
            self.points.append([self.calc_height(value) for value in args])
            if len(self.points) % 20 == 0 and self.line_width > 0.2:
                self.line_width -= 0.1

        n = len(self.points) - 1
        x_scale = (self.w - self.x_padding) / (n if n else 1)
        x = self.x_padding
        lasts, last_x = self.points[0], self.x_padding
        for points in self.points:
            self.draw_points(last_x, x, lasts, points, colors)
            lasts, last_x = points, x
            x += x_scale

        self.add_info(self.optimizer.round, self.optimizer.record.score)

    def add_info(self, rnd, score):
        x, y = self.w - 150, 80
        self.add_text(f'round: {rnd}', x, y)
        self.add_tick(score)

    def add_text(self, text, x, y):
        self.canvas.create_text(x, y, text=text, font=self.font, fill='black', tags=('to delete',))

    def add_tick(self, point):
        y = self.calc_height(point)
        d = self.x_padding / 4
        self.canvas.create_line(self.x_padding - d, y, self.x_padding + d, y,
                                fill='black', width=self.line_width, tags=('to delete',))

    def draw_axes(self):
        floor = self.h - self.y_padding
        self.canvas.create_line(self.x_padding, 0, self.x_padding, floor,
                                fill='black', width=self.line_width)
        self.canvas.create_line(self.x_padding, floor, self.w, floor,
                                fill='black', width=self.line_width)


class RecordHolder:
    def __init__(self, obj, score, info, minimize=False):
        self.obj, self.score, self.info = obj, score, info
        self.cmp = (lambda x, y: x > y) if minimize else (lambda x, y: x < y)

    def compare(self, score, obj, info):
        if self.score is not None and self.cmp(score, self.score):
            return

        self.obj, self.score, self.info = obj, score, info
