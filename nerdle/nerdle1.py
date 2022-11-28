from pprint import pprint
from tkinter import Tk, Canvas
from itertools import product


class Bot:
    def __init__(self, length):
        if type(length) == list:
            self.answers = length
        else:
            self.answers = get_permutations(length)
        self.random_threshold = 3
        print(self.answers)

        from random import choice
        self.best = ''  # random for speed, find later
        print('finished getting answers')

        r = 1
        while True:  # TODO: make a gui
            guess, result = (lambda a: (*a,) + tuple([''] * (2 - len(a))) if len(a) != 2 else a)(input('guess? (leave blank for best choice): ').split())
            if guess == 'gg':
                break

            print(guess, result)
            if not result:
                print(f'using {(self.best, result)} as guess')
                guess, result = self.best, guess

            self.answers = self.eliminate_guesses(guess, list(map(int, result)))

            self.score_guesses()

            self.best = self.answers[0]
            print(f'best guess: "{self.best}" ({", ".join(self.answers[:3])})\nremaining: {len(self.answers)}')

    def eliminate_guesses(self, guess, result, l=None):  # use a min-max like search, cancel out by first to last
        return [a for a in (self.answers if not l else l) if self.get_output(guess, a) == result]

    def score_guesses(self):
        scores = {}
        length = len(self.answers)
        for guess in self.answers:
            scores[guess] = sum(len(self.eliminate_guesses(guess, self.get_output(guess, ans))) - length for ans in self.answers)
        self.answers = sorted(self.answers, key=lambda x: scores[x])

    @staticmethod
    def get_output(guess, answer):
        r, answer = [0] * len(guess), list(answer)

        for i, (gl, al) in enumerate(zip(guess, answer)):
            if gl == al:
                r[i] = 2
                answer[i] = ''

        for i, l in enumerate(guess):
            if not answer[i]:
                continue

            if l in answer:
                r[i] = 1
                answer[answer.index(l)] = ''
            else:
                r[i] = 0
        return r


def test_equation(equation):
    rhs, lhs = equation.split('=')
    if any(a * 2 in equation for a in '+-/=*'):
        return False
    if any('/0' in x or not x or x in '-+=*/' for x in (rhs, lhs)):
        return False
    try:
        exec(f'1 / (({lhs}) - ({rhs}))')
    except ZeroDivisionError:
        return True
    except Exception:
        return False
    return False


def get_permutations(length):
    """
    a valid equation will always have the lhs and right hand side equal, so lhs - rhs will be 0
    we can exploit this to get an error when running exec(" 1 / (lhs - rhs) "),
    this way we dont have to code a parser for math eq

    a valid solution will have all operations on the lhs, so we remove those to filter for solutions only
    """

    eq = product('1234567890-+*/=', repeat=length)
    for string in eq:
        string = ''.join(string)
        if len(string.split('=')) != 2:
            continue
        if not test_equation(string):
            continue
        if any(x in string.split('=')[1] for x in '-+/*'):
            continue

        yield string

    return None


class Node:
    def __init__(self, parent, value):
        self.children = []
        self.parent = parent
        if self.parent is not None:
            self.parent.children.append(self)
        self.value = value

    def remove(self):
        if self.parent is not None:
            self.parent.children.remove(self)
        del self

    def __repr__(self):
        return self.value

    @property
    def length(self):
        if not self.children:
            return 0

        return sum(1 + c.length for c in self.children)

    def add(self, value):
        Node(self, value)


class Tree:
    def __init__(self, length=3):
        parent = Node(None, None)

        layer = first = [Node(parent, char) for char in '1234567890-+*/']
        for depth in range(1, length):
            new_l = []
            for node in layer:
                for char in '1234567890-+*/':
                    new_l.append(Node(node, char))
            layer = new_l

        print(parent.length)

        guess, answer = input().split()
        for i, a in enumerate(answer):
            if a == '0':
                for node in first:
                    if node.value == guess[i]:
                        node.remove()
                        break

        print(parent.length)


class Display:
    @staticmethod
    def create_block(window, index, color='grey'):
        x = index * 200
        window.create_rectangle(x, 0, x + 200, 100, fill=color, tags=(str(index),))

    def __init__(self, cls, length):
        self.root = Tk()
        self.root.geometry(f'{length * 200}x{100}')

        self.canvas = Canvas(self.root, width=length * 200, height=100, bg='white')
        self.canvas.pack()
        self.colors = ['grey' for _ in range(length)]

        for i in range(length):
            self.create_block(self.canvas, i)

    def cycle(self, index):
        self.canvas.delete(str(index))
        c = {'grey':'yellow',
             'yellow':'green',
             'green':'grey'}[self.colors[index]]
        self.create_block(self.canvas, index, color=c)
        self.colors[index] = c


if __name__ == '__main__':
    Tree()
    func = lambda n: sum(n ** k for k in range(n))

    exit()

    Bot(8)
