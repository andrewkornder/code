from random import choice, shuffle, randint
from json import load
from os import walk, path, listdir
from ml.genetic_algorithm import Graph


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
    def sample_text(*_):  # 35 chars
        return Text.cleanup('The quick brown fox jumps over the lazy dog')

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
    letters = list('abcdefghijklmnopqrstuvwxyz;,./')
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
        for i, letter in enumerate(cls.letters):
            keys[letter] = (x, y)
            x += 1
            if x == 10:
                x = 0
                y += 1

        return cls(keys)

    @classmethod
    def merge(cls, a, b, swaps=True):
        def swap(dictionary):
            items = list(dictionary.items())
            (l0, e0), (l1, e1) = choice(items), choice(items)
            dictionary[l1] = e0
            dictionary[l0] = e1

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
                keys[letter] = (x, y)
                remaining_letters.remove(letter)

        for x, y in missing:
            letter = choice(remaining_letters)
            keys[letter] = (x, y)
            remaining_letters.remove(letter)

        if swaps:
            choices = [0, 0] + list(range(randint(0, 3)))
            for _ in range(choice(choices)):
                swap(keys)

        return cls(keys)

    @classmethod
    def merge_b(cls, a, b, swaps=True):  # maybe put all keys where a and b agree, randomize rest?
        # maybe just 50/50 on every key if possible, then just pick a random key or sum

        if swaps:
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
        for letter, coords in b._k.items():
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

        if swaps:
            k = {v: k for k, v in keys.items()}
            choices = [0, 0] + list(range(randint(0, 3)))
            for _ in range(choice(choices)):
                swap()
            keys = {v: k for k, v in k.items()}

        return cls(keys)

    def get_distance(self, x0, y0, x1, y1):
        dx = x0 - x1  # if dx > 0, moved left, else moved right
        dy = y0 - y1  # if dy > 0, moved down, else up

        # what the fuck
        return self.hard_coded_distance[(x0, y0, x1, y1)] if dx and dy else \
            (dy == 0) * abs(dx) + (dy != 0) * (1 + 0.5 * (x0 in (0, 9))) * \
            (2.138 * (dy == 2) + (dy != 2) * 1.118 - 0.086 * (0 in (y1, y0)))

    def get_distance2(self, x0, y0, x1, y1):
        dx = x0 - x1  # if dx > 0, moved left, else moved right
        dy = y0 - y1  # if dy > 0, moved down, else up

        if dy == 0:
            return abs(dx)

        if dx == 0:  # what the fuck
            return (1 + 0.5 * (x0 in (0, 9))) * (2.138 * (dy == 2) + (dy != 2) * 1.118 - 0.086 * (0 in (y1, y0)))

        return self.hard_coded_distance[(x0, y0, x1, y1)]

    def fitness_score(self, text):
        distance = 0
        last = self.fingers[0]  # doesnt really matter which one, wont change the outcome
        for char in text:
            x, y = self.keys(char)
            finger = self.fingers[x]

            distance += self.get_distance(finger.x, finger.y, x, y)

            if finger != last:
                last.reset()
            last = finger

        return distance

    def __str__(self):
        return '\n'.join(' '.join(self.coords(x, y) for x in range(10)) for y in range(3))

    def get_format(self):
        return ''.join(''.join(self.coords(x, y) for x in range(10)) for y in range(3))

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

    def m(x): return -0.5 + sqrt(1 + 8 * m_k * x) / 2  # p_size for some multiple of m_k

    k = 0
    for i in range(n):
        while True:
            k += 1
            q = m(k)
            if q.is_integer():
                print(q, m_k * k)  # p_size, population_size
                break


if __name__ == '__main__':
    # get_p_size_splits(5, 100)
    t, test = get_text(), Text.wikipedia_text(1000000)

    best = Keyboard.get_best()
    heights = [Keyboard.qwerty().fitness_score(t),
               Keyboard.rstlne().fitness_score(t),
               best.fitness_score(t)]

    current_best = Graph(Keyboard, t, size=len(t), comparisons=heights,
                         minimize=True, text_output=True, full_refresh=True).run()
    if current_best.fitness_score(test) < best.fitness_score(test):
        open('best.txt', 'w').write(current_best.get_format())
        print('new best:\n' + str(current_best))
