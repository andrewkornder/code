from random import shuffle, randint, choice, sample
from os import walk, listdir, path
from json import load
from threading import Thread
from tkinter import Canvas, Tk, Button, Label, StringVar
from time import time, sleep

# TODO: honestly just remake the entire thing with a nested list for the self.keys, since itd be sm easier to work with
#       could be slower tho


class App:
    def __init__(self, w=1350, h=900):
        self.optimizer = Optimizer(show_progress=None)

        self.x_padding, self.y_padding = w // 50, h // 50

        self.y_scale, self.y_floor = 0, 0
        self.point_size = 2
        self.line_width = 3
        self.colors = ['blue', 'red', 'dark green']

        self.w, self.h = w + 2 * self.x_padding, h + 2 * self.y_padding
        self.bests = []
        self.averages = []

        self.root = Tk()
        self.root.geometry(f'{self.w}x{self.h + 100}+50+10')
        self.root.bind('<space>', self.toggle_state)

        self.running = StringVar(self.root, value='stopped')

        self.canvas = Canvas(self.root, height=h + 2 * self.y_padding, width=w + 2 * self.x_padding, bg='white')
        self.canvas.grid(column=0, row=0, columnspan=3)

        # placeholders
        self.start_button, self.stop_button, self.state_label, self.round_label, self.quit_button = 0, 0, 0, {'': ''}, 0
        self.widgets = []
        self.create_widgets()

        self.draw_axes()
        self.set_scale()
        for name, (_, score) in self.optimizer.set_ups.items():
            self.add_comparison(score)  # should set qwerty to be the setting value for the scale

        self.loop()
        self.root.mainloop()

    def create_widgets(self):
        self.start_button = Button(text='start', command=self.start)
        self.start_button.grid(column=0, row=1)
        self.widgets.append(self.start_button)

        self.stop_button = Button(text='stop', command=self.stop)
        self.stop_button.grid(column=2, row=1)
        self.widgets.append(self.stop_button)

        self.state_label = Label(textvariable=self.running)
        self.state_label.grid(column=0, row=2)
        self.widgets.append(self.state_label)

        self.round_label = Label(text='round 0')
        self.round_label.grid(column=1, row=2)
        self.widgets.append(self.round_label)

        self.quit_button = Button(text='quit', command=self.quit)
        self.quit_button.grid(column=2, row=2)
        self.widgets.append(self.quit_button)

    def loop(self):
        if self.running.get() == 'stopped':
            return self.root.after(1, self.loop)

        self.optimizer.run()
        self.draw_graph(self.optimizer.scores[0], self.optimizer.average)
        self.round_label['text'] = f'round {self.optimizer.i}'

        self.root.after(1, self.loop)

    def calc_height(self, y):
        return self.h + (self.y_floor - y) * self.y_scale - self.y_padding

    def draw_graph(self, best, average):
        self.bests.append(self.calc_height(best))
        self.averages.append(self.calc_height(average))

        self.canvas.delete('lines')
        self.canvas.delete('points')
        self.canvas.delete('ticks')

        x_scale = (self.w - 2 * self.x_padding) / len(self.bests)
        lw = round(self.line_width - (0.1 * self.optimizer.i // 100), 2) if \
            self.optimizer.i < 100 * self.line_width else 0.1
        ps = round(self.point_size - (0.1 * self.optimizer.i // 200), 2) if \
            self.optimizer.i < 200 * self.line_width else 0.1

        for i, points in enumerate((self.bests, self.averages)):
            last = self.x_padding, points[0]
            x = self.x_padding
            for j, y in enumerate(points):
                self.canvas.create_line(*last, x, y, fill=self.colors[i], width=lw, tags=('lines',))
                self.canvas.create_oval(x - ps, y - ps,
                                        x + ps, y + ps,
                                        fill=self.colors[i], outline='', tags=('points',))

                last = x, y
                x += x_scale

        self.add_tick(self.optimizer.best_score)

    def set_scale(self):
        chars = len(self.optimizer.text)

        self.y_scale = (0.9 * self.h) / chars
        self.canvas.create_text(self.x_padding + 50, self.y_padding + 10, text=str(chars), font=('Niagara Bold', 10))

        self.y_floor = 0.25 * chars

    def add_comparison(self, height):
        y = self.calc_height(height)
        self.canvas.create_line(self.x_padding, y, self.w - self.x_padding, y,
                                width=self.line_width, fill=self.colors[2])

    def add_tick(self, height):
        y = self.calc_height(height)
        self.canvas.create_line(self.x_padding - 5, y, self.x_padding + 5, y,
                                width=self.line_width, fill='black', tags=('ticks',))

    def draw_axes(self):
        floor = self.h - self.y_padding
        # y axis
        self.canvas.create_line(self.x_padding, self.y_padding, self.x_padding, floor,
                                width=self.line_width, fill='black')
        # x axis
        self.canvas.create_line(self.x_padding, floor, self.w - self.x_padding, floor,
                                width=self.line_width, fill='black')

    def start(self):
        self.running.set('running')

    def stop(self):
        self.running.set('stopped')

    def toggle_state(self, _):
        self.running.set('stopped' if self.running.get() == 'running' else 'running')

    def quit(self):
        self.running.set('stopped')

        print(
            f'''================DONE================
total time: {time() - self.optimizer.start_time}
final score (from round {self.optimizer.best_round} / {self.optimizer.i}): {self.optimizer.best_score}

{self.optimizer.best.get_format()}''')

        for widget in self.widgets:
            widget.destroy()


QWERTY = 'qwertyuiopasdfghjkl;zxcvbnm,./'
RSTLNE = 'fghcz;wmpueasndlrtio,qvb/yxkj.'


def convert_to_coords(key, letters=QWERTY):
    i = letters.find(key)
    return i % 10, i // 10


class Finger:
    def __init__(self, x, y, keys):
        self.x, self.y, self.keys = x, y, keys
        self.default = x, y

    @property
    def coords(self):
        return self.x, self.y


class Keyboard:
    y_dist = {1: 1.032,
              2: 2.138,
              -2: 2.138,
              -1: 1.118}

    xy_dist = {(3, 0, 4, 1): 1.605,
               (3, 0, 4, 2): 2.661,
               (3, 1, 4, 0): 1.247,
               (3, 1, 4, 2): 1.803,
               (3, 2, 4, 0): 2.015,
               (3, 2, 4, 1): 1.118,
               (4, 0, 3, 1): 1.247,
               (4, 0, 3, 2): 2.015,
               (4, 1, 3, 0): 1.605,
               (4, 1, 3, 2): 1.118,
               (4, 2, 3, 0): 2.661,
               (4, 2, 3, 1): 1.803,
               (5, 0, 6, 1): 1.605,
               (5, 0, 6, 2): 2.661,
               (5, 1, 6, 0): 1.247,
               (5, 1, 6, 2): 1.803,
               (5, 2, 6, 0): 2.015,
               (5, 2, 6, 1): 1.118,
               (6, 0, 5, 1): 1.247,
               (6, 0, 5, 2): 2.015,
               (6, 1, 5, 0): 1.605,
               (6, 1, 5, 2): 1.118,
               (6, 2, 5, 0): 2.661,
               (6, 2, 5, 1): 1.803}

    @staticmethod
    def get_distance(x0, y0, x1, y1):  # dy < 0 means moves down, dx < 0 means moves right
        if (x0, y0) == (x1, y1):
            return 0

        dy = y0 - y1
        if not dy:
            return 1

        dx = x0 - x1
        if not dx:  # should only be false if the movement is a diagonal move from the center
            return Keyboard.y_dist[dy]
        # now the only possible values are -1 and 1 for dx and dy

        return Keyboard.xy_dist[(x0, y0, x1, y1)]

    ownership = {a: [[(0, 0), (0, 1), (0, 2)],
                     [(1, 0), (1, 1), (1, 2)],
                     [(2, 0), (2, 1), (2, 2)],
                     [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2)],
                     [],
                     [],
                     [(5, 0), (5, 1), (5, 2), (6, 0), (6, 1), (6, 2)],
                     [(7, 0), (7, 1), (7, 2)],
                     [(8, 0), (8, 1), (8, 2)],
                     [(9, 0), (9, 1), (9, 2)]][a] for a in range(10) if a not in (4, 5)}

    r_own = {}
    for f, l in ownership.items():
        for cc in l:
            r_own[cc] = f

    letters = 'abcdefghijklmnopqrstuvwxyz;,./'

    def __init__(self, keys):
        self.fingers = {a: Finger(a, 1, self.ownership[a]) for a in range(10) if a not in (4, 5)}

        # keys is (letter) => (x, y)
        # coords is (x, y) => (letter)
        self.keys = keys  # defined in merge or random start
        self.c = {v: k for k, v in self.keys.items()}

    @classmethod
    def from_string(cls, string):
        return Keyboard({letter: convert_to_coords(letter, string) for letter in string})

    @classmethod
    def randomize(cls):
        keys = {}
        order = sample(cls.letters, 30)
        for i, l in enumerate(order):
            keys[l] = i % 10, i // 10
        return Keyboard(keys)

    @classmethod
    def merge(cls, a, b, r=True, randomness=3, swaps=3):  # maybe put all keys where a and b agree, randomize rest?
        # maybe just 50/50 on every key if possible, then just pick a random key or sum

        if r:
            ab = [a, b]
            shuffle(ab)
            a, b = ab

        def swap():
            x0, x1 = randint(0, 4), randint(5, 9)
            y0, y1 = randint(0, 2), randint(0, 2)
            placeholder = k[(x0, y0)]
            k[(x0, y0)] = k[(x1, y1)]
            k[(x1, y1)] = placeholder

        keys = {letter: None for letter in cls.letters}

        for x in range(5):
            for y in range(3):
                keys[a.coords(x, y)] = (x, y)

        ml = []
        for letter, coords in b.keys.items():
            if keys[letter] is not None:
                continue

            if coords[0] > 4:
                keys[letter] = coords
            else:
                ml.append(letter)

        m = [(x, y) for x in range(5, 10) for y in range(3) if (x, y) not in keys.values()]
        for letter in ml:
            c = choice(m)
            m.remove(c)
            keys[letter] = c

        if r and randomness:
            k = {v: k for k, v in keys.items()}
            for _ in range(choice([0] * (10 - randomness) + list(range(swaps)))):
                swap()
            keys = {v: k for k, v in k.items()}

        return Keyboard(keys)

    def coords(self, x, y):
        return self.c[(x, y)]

    def fitness_score(self, text):
        distance = 0
        last = None
        for letter in text:
            xy = self.keys[letter]
            finger = self.fingers[self.r_own[xy]]
            if last is not finger and last is not None:
                last.x, last.y = last.default

            distance += self.get_distance(finger.x, finger.y, *xy)
            finger.x, finger.y = xy
            last = finger

        return distance

    def copy(self):
        return Keyboard(self.keys.copy())

    def get_format(self):
        s = ' '
        for y in range(3):
            s += '_' * 39 + '\n'
            for x in range(10):
                s += f'| {self.coords(x, y).upper()} '
            s += '|\n '

        return s + '_' * 39

    def get_format2(self):
        return '\n'.join(''.join(self.coords(x, y) for x in range(10)) for y in range(3))


class Optimizer:
    @staticmethod
    def cleanup(string):
        return ''.join(char for char in string.lower() if char in 'abcdefghijklmnopqrstuvwxyz;,./').replace('?', '/')

    @staticmethod
    def get_code(t=True):  # if t = True, returns 4,800,000 chars, else returns 260,000
        def get_files(folder):
            total = []

            files = list(walk(folder))
            for subfolder in files:
                total += [path.join(subfolder[0], f) for f in subfolder[2] if f[-3:] == '.py']

            return total if t else [file for file in total if 'venv' not in file]

        return Optimizer.cleanup(''.join(open(file, errors='ignore').read() for file in get_files('../')))

    @staticmethod
    def sample_text(*_):  # 35 chars
        return Optimizer.cleanup('The quick brown fox jumps over the lazy dog')

    @staticmethod
    def wikipedia_text(length, folder='E:/resources/wiki_text'):
        string = ''
        for file_path in listdir(folder):
            file = load(open(f'{folder}/{file_path}', encoding='utf-8'))
            for excerpt in file:
                text = excerpt['text']
                string += Optimizer.cleanup(text)

                if len(string) > length:
                    return string[:length]

        return string

    @staticmethod
    def letter_freq(t, top_n=10):
        f = {letter: 0 for letter in 'abcdefghijklmnopqrstuvwxyz;,./'}
        length = len(t)
        for char in t:
            f[char] += 1

        for letter, freq in f.items():
            f[letter] = freq / length

        sorted_f = [(a, round(b, 3)) for a, b in sorted(f.items(), key=lambda x: x[1])]
        return sorted_f[-top_n:][::-1]

    @staticmethod
    def get_text_choice(funcs):
        func_choice = int(input('text?\n' + ''.join(f'{n + 1} : {func.__name__}\n' for n, func in enumerate(funcs))))
        args = []
        if func_choice == 3:
            args = [int(input('how many characters?\n'))]
        elif func_choice == 2:
            args = [input('take all code?\n') == 'yes']

        return func_choice, args

    def __init__(self, rounds=1000, population_size=120,
                 p_size=16, show_progress: int | None = 2, text_choice=None):
        # show_progress is False, True, and None (None shows zero output, not even the finished keyboard

        self.text_choices = [self.sample_text, self.get_code, self.wikipedia_text]

        self.rounds, self.population_size, self.p_size = rounds, population_size, p_size

        self.i = 0

        func_choice, args = self.get_text_choice(self.text_choices) if text_choice is None else text_choice
        self.text = self.text_choices[func_choice - 1](*args)

        if show_progress:
            print(*self.letter_freq(self.text))

        self.visible_progress = show_progress

        self.set_ups = {'qwerty': Keyboard.from_string(QWERTY),
                        'rstlne': Keyboard.from_string(RSTLNE)}
        self.set_ups = {k: (v, v.fitness_score(self.text)) for k, v in self.set_ups.items()}

        print('\n'.join(f'{name}: {score:.3f}' for name, (_, score) in self.set_ups.items()))

        starting_kb = input('specific starting keyboards?\n')
        if starting_kb in self.set_ups:
            self.gen = self.starting_seed(QWERTY if starting_kb == 'qwerty' else RSTLNE)
        elif len(starting_kb) != 30:
            self.gen = [Keyboard.randomize() for _ in range(self.population_size)]
        else:
            self.gen = self.starting_seed(starting_kb)

        self.last_best = 0
        self.randomness = 3
        self.change_randomness = bool(input('variable randomness?\n'))

        self.scores = []
        self.average = 0
        self.best, self.best_score, self.best_round = None, 1 << 63, 0

        self.start_time = None

    def full_run(self):
        for i in range(self.rounds):
            self.run()

    def run(self):
        if not self.i:
            self.start_time = time()

        self.i += 1

        top, score = self.get_new_generation()
        if score <= self.best_score:
            self.best, self.best_score, self.best_round = top, score, self.i

        if self.change_randomness:
            convergence = score - self.last_best
            self.last_best = score
            if abs(convergence) < 0.001 * score and self.randomness < 10:
                self.randomness += 1
            elif convergence > 0.1 * score:
                self.randomness -= 1

        if self.visible_progress:
            print(f'\r{self.i / 10:>5.1f}% | {score:.3f} | {self.average:.3f}', end='')

        if self.i == self.rounds and self.visible_progress is not None:
            print('\n================DONE================')

            final_kb, final_score = self.get_best_keyboards()[0], self.scores[0]
            if final_score <= self.best_score:
                self.best, self.best_score, self.best_round = final_kb, final_score, self.i

            print(self.final_output())

    def starting_seed(self, template):
        def rand_swap(kb):
            k = kb.keys
            l1, l2 = sample(Keyboard.letters, 2)

            placeholder = k[l1]
            k[l1] = k[l2]
            k[l2] = placeholder

        def change(kb):
            for _ in range(randint(1, 4)):
                rand_swap(kb)

            return kb

        default = Keyboard.from_string(template)
        keyboards = [change(default.copy()) for _ in range(self.population_size)]
        return keyboards

    def get_new_generation(self):
        top = self.get_best_keyboards()
        self.combine_old_gen(top)

        return top[0], self.scores[0]

    def get_best_keyboards(self):
        def thread_score(keyboard):
            score = keyboard.fitness_score(self.text)
            total[0] += score
            scores[keyboard] = score

        scores = {}
        total = [0]  # lists can be changed in thread_score without losing the information ig?

        last = None
        for kb in self.gen:
            last = Thread(target=thread_score, args=(kb,))
            last.start()
        while last.is_alive():
            sleep(0.1)

        self.average = total[0] / self.population_size
        top, self.scores = list(zip(*sorted(scores.items(), key=lambda a: a[1])[:self.p_size]))
        return top

    # TODO: weight successful keyboards so they have more offspring in the next gen?
    def combine_old_gen(self, population):
        self.gen = []
        for i, a in enumerate(population):  # TODO: think about how many swaps
            self.gen.extend(
                Keyboard.merge(a, b, r=True, randomness=self.randomness, swaps=3) for b in population[i + 1:])

    def final_output(self):
        return f'''{'total time (m):':<30}{(time() - self.start_time) / 60:>10.1f}
{f'final score (from round{self.best_round}):':<30}{self.best_score:>10.3f}

{self.best.get_format()}'''


if __name__ == '__main__':
    # opt = Optimizer()
    # opt.full_run()

    App()
