from random import choice, shuffle, randint, sample
from json import load
from os import walk, path, listdir
from ml.genetic_algorithm import Graph, Optimizer
import numpy as np
from math import dist as distance


class Text:
    @staticmethod
    def cleanup(string):
        return ''.join(char for char in string.lower() if char in 'abcdefghijklmnopqrstuvwxyz;,./').replace('?', '/')

    @staticmethod
    def get_code(length, all_text=False):  # if t = True, returns 4,800,000 chars, else returns 260,000
        def get_files(folder):
            total = []

            files = list(walk(folder))
            for subfolder in files:
                total += [path.join(subfolder[0], f) for f in subfolder[2] if f[-3:] == '.py']

            return total if all_text else [file for file in total if 'venv' not in file]

        return Text.cleanup(''.join(open(file, errors='ignore').read() for file in get_files('E:/all')))[:length]

    @staticmethod
    def sample_text(*_):  # 32 chars, 2 e's, 2 u's, 3 o's and 3 i's
        return 'packmyboxwithfivedozenliquorjugs'

    @staticmethod
    def wikipedia_text(length, folder='E:/resources/wiki_text'):
        string = ''
        for json in listdir(folder):
            file = load(open(f'{folder}/{json}', encoding='utf-8'))
            for entry in file:
                excerpt = entry['text']
                string += Text.cleanup(excerpt)

                if len(string) > length:
                    return string[:length]

        return string


class Finger:
    def __init__(self, x, y):
        self.default = x, y
        self.x, self.y = x, y

    def reset(self):
        self.x, self.y = self.default


class Keyboard:
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', ';', ',', '.', '/']

    hard_coded_distance = {(3, 0, 4, 1): 1.605,
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

    def __init__(self, keys):
        self._k = keys  # str -> x, y
        self._c = {v: k for k, v in keys.items()}  # x, y -> str

        self.fingers = {a: Finger(a, 1) for a in (0, 1, 2, 3, 6, 7, 8, 9)}
        self.fingers[4] = self.fingers[3]
        self.fingers[5] = self.fingers[6]

    def coords(self, x, y):
        return self._c[(x, y)]

    def keys(self, char):
        return self._k[char]

    @classmethod
    def randomize(cls):
        keys = {}

        shuffle(cls.letters)

        x, y = 0, 0
        for letter in cls.letters:
            keys[letter] = x, y
            x += 1
            if x == 10:
                x = 0
                y += 1

        return cls(keys)

    @classmethod
    def merge(cls, a, b):
        def swap(dictionary):
            (l0, e0), (l1, e1) = sample(list(dictionary.items()), 2)
            dictionary[l1], dictionary[l0] = e0, e1

        keys = {}
        remaining_letters = cls.letters[:]
        missing = []
        for y in range(3):
            for x in range(10):
                alleles = a.coords(x, y), b.coords(x, y)
                validity = [allele not in keys for allele in alleles]

                if not any(validity):
                    missing.append((x, y))
                    continue

                letter = choice([l for v, l in zip(validity, alleles) if v])
                keys[letter] = x, y

                remaining_letters.remove(letter)

        shuffle(remaining_letters)
        for c in missing:
            keys[remaining_letters.pop()] = c

        for _ in range(np.random.choice([0, 1, 2, 3], p=[0.5, 0.17, 0.17, 0.16])):
            swap(keys)

        return cls(keys)

    @classmethod
    def merge_b(cls, a, b):
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

        ml = []  # think about whether starting empty and adding letters or starting w b._k.keys() is better
        mc = [(x, y) for x in range(5, 10) for y in range(3)]
        for letter, coords in b._k.items():
            if keys[letter] is not None:
                continue

            if coords[0] > 4:
                keys[letter] = coords
                mc.remove(coords)
            else:
                ml.append(letter)

        shuffle(mc)
        for letter in ml:
            keys[letter] = mc.pop()

        # TODO: switch the order from line 158 and then reverse back at line 184, avoiding line 180
        k = {v: k for k, v in keys.items()}
        for _ in range(np.random.choice([0, 1, 2, 3], p=[0.5, 0.17, 0.17, 0.16])):
            swap()

        return cls({v: k for k, v in k.items()})

    @classmethod
    def merge_c(cls, a, b):
        def swap(dictionary):
            (l0, e0), (l1, e1) = sample(list(dictionary.items()), 2)
            dictionary[l1], dictionary[l0] = e0, l1

        ml = []
        mc = [(x, y) for x in range(10) for y in range(3)]
        keys = {}
        for letter in Keyboard.letters:
            ak = a.keys(letter)
            if ak == b.keys(letter):
                keys[letter] = ak
                mc.remove(ak)
                continue
            ml.append(letter)

        shuffle(mc)
        for letter in ml:  # todo: weight choices someone so the key is more likely to stay where it was
            keys[letter] = mc.pop()

        for _ in range(np.random.choice([0, 1, 2, 3], p=[0.5, 0.17, 0.17, 0.16])):
            swap(keys)

        return cls(keys)

    def get_distance(self, x0, y0, x1, y1):
        dx, dy = x0 - x1, y0 - y1

        # what the fuck
        return self.hard_coded_distance[(x0, y0, x1, y1)] if dx and dy else \
            (dy == 0) * abs(dx) + (dy != 0) * (1 + 0.5 * (x0 in (0, 9))) * \
            (2.138 * (dy == 2) + (dy != 2) * 1.118 - 0.086 * (0 in (y1, y0)))

    def fitness_score(self, text):
        distance, last = 0, self.fingers[0]  # doesnt really matter which one, wont change the outcome
        for x, y in (self.keys(char) for char in text):
            finger = self.fingers[x]
            distance += self.get_distance(finger.x, finger.y, x, y)

            if finger != last:
                last.reset()
                last = finger

        return distance

    def __str__(self):
        return '\n'.join(' '.join(self.coords(x, y) for x in range(10)) for y in range(3))

    @classmethod
    def from_string(cls, string):
        return cls({letter: (i % 10, i // 10) for i, letter in enumerate(string)})

    @classmethod
    def qwerty(cls):
        return cls.from_string('qwertyuiopasdfghjkl;zxcvbnm,./')

    @classmethod
    def rstlne(cls):
        return cls.from_string('fghcz;wmpueasndlrtio,qvb/yxkj.')

    @classmethod
    def custom_rstlne(cls):
        return cls.from_string('qwdfz;ukypaserlhniotgxcv/bjm,.')

    @classmethod
    def get_best(cls, file='best.txt'):
        return cls.from_string(open(file).read())

    def distance_from_qwerty(self):
        return sum(distance(self.keys(char), (i % 10, i // 10)) for i, char in enumerate('qwertyuiopasdfghjkl;zxcvbnm,./'))


def get_text():
    choices = {'wiki': Text.wikipedia_text,
               'code': Text.get_code,
               '': Text.sample_text}

    func = input('what text? ').strip()
    if func.isnumeric():
        return Text.wikipedia_text(int(func))
    return choices[func](int(input('length of text? ')) if func else 1000)


def get_p_size_splits(m_k, n):
    from math import sqrt

    def m(x):
        return -0.5 + sqrt(1 + 8 * m_k * x) / 2  # p_size for some multiple of m_k

    k = 0
    for i in range(n):
        while True:
            k += 1
            q = m(k)
            if q.is_integer():
                print(q, m_k * k)  # p_size, population_size
                break


def fin(best):
    t = Text.wikipedia_text(1000000)
    b = Keyboard.get_best()
    if best.fitness_score(t) <= b.fitness_score(t) and \
       best.distance_from_qwerty() < b.distance_from_qwerty():
        open('keyboard/best.txt', 'w').write(best.get_format())
        print('new best:\n' + str(best))


def t_output(text, i):
    best = Optimizer(Keyboard, text, minimize=True).run(i)
    fin(best)


def graph(text):
    best = Keyboard.get_best()
    heights = [Keyboard.qwerty().fitness_score(text),
               Keyboard.rstlne().fitness_score(text),
               best.fitness_score(text)]

    current_best = Graph(Keyboard, text, size=len(text), comparisons=heights,
                         minimize=True, text_output=True, full_refresh=1).run()
    fin(current_best)


if __name__ == '__main__':
    t_output(get_text(), 300)