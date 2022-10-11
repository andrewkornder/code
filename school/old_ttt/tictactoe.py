import tkinter
from pprint import pprint
from itertools import chain


def all_moves(game):
    return [(a, b) for a in range(len(game)) for b in range(len(game)) if not game[a][b]]


class Node:
    def __init__(self, moves, previous, n=None, score=0):
        self.prev = previous
        self.moves = moves
        self.score = score
        self.best = None
        if n is None:
            self.next = []
        else:
            self.next = n

    def get_board(self, board, turn):
        copy = [arr[:] for arr in board]
        for r, c in self.moves:
            copy[r][c] = turn + 1
            turn = not turn
        return copy

    def __repr__(self):
        return f'{self.moves} -> {self.score}'


class Bot:
    def __init__(self, game):
        self.game = game
        self.size = game.size
        self.tree = []

    def move(self):
        if all(sum(row) == 0 for row in self.game.array):
            return self.game.size // 2, self.game.size // 2

        top = Node([], None)
        turn = self.game.turn

        layers = {}
        for depth in range(self.game.length + 2):
            layer = []
            for node in (layers[depth - 1] if layers else (top,)):
                if node.score == 0:
                    layer += self.branch(node, turn)
            layers[depth] = layer
            turn = not turn

        self.score_branches(layers, self.game.turn)

        top_layer = layers[0]
        best = min(top_layer, key=lambda n: n.score)
        return best.moves[0]

    def score_branches(self, layers, turn):
        for depth in layers:
            layer = layers[depth]
            for node in layer:
                if node.next:
                    node.best = (max if turn is self.game.turn else min)(node.next, key=lambda x: x.score)
                    node.score = node.best.score
        pprint(layers, depth=1000)

    def branch(self, node, turn):
        """
        creates a branch of the minimax tree that starts at a certain node.
        each node is a list of moves to get to that board position.
        
        :param turn: the turn
        :param node: the previous mode to expand on
        """

        copy = node.get_board(self.game.array, self.game.turn)
        for move in all_moves(copy):
            n = Node(node.moves + [move], node)
            c, p = check_win(n.get_board(self.game.array, self.game.turn), self.game.length, turn)
            n.score = c * (-1 + 2 * p)
            node.next.append(n)

        return node.next


class Game:
    def __init__(self, size=3, length=3, window_size=(150, 150), text=(' ', 'x', 'o')):
        self.scale_x, self.scale_y = window_size
        self.win_width, self.win_height = self.scale_x * size, self.scale_y * size
        self.size = size

        self.root = tkinter.Tk()
        self.root.geometry(f'{self.win_width}x{self.win_height}')

        self.canvas = tkinter.Canvas(self.root, bg='white', height=self.win_height, width=self.win_width)
        self.canvas.pack()

        self.draw_lines(size)
        self.bindings()

        self.array = [[0] * size for _ in range(size)]
        self.translate = dict(zip(range(3), text, strict=True))
        self.reverse_trans = {v: k for k, v in self.translate.items()}

        self.turn = False  # true for p1, False for p2

        self.bot = Bot(self)
        self.pvp = False

        self.length = length

    def switch_opponent(self):
        self.pvp = not self.pvp

    def bindings(self):
        b = [(self.canvas, 'Button-1', lambda e: self.move(e.y // self.scale_y, e.y // self.scale_x)),
             (self.root, 'Return', lambda e: self.switch_opponent()),
             (self.canvas, 'Button-3', lambda e: self.reset())]

        for widget, seq, func in b:
            widget.bind(f'<{seq}>', func)

    def draw_lines(self, size):
        for i in range(1, size + 1):
            a, b = i * self.scale_x, i * self.scale_y
            self.canvas.create_line(a, 0, a, self.win_height, fill='black', tags=('lines',))
            self.canvas.create_line(0, b, self.win_width, b, fill='black', tags=('lines',))

    def display(self):
        self.canvas.delete('text')

        for r, row in enumerate(self.array):
            y = (r + .5) * self.scale_y
            for c, value in enumerate(row):
                x = (c + .5) * self.scale_x
                self.canvas.create_text(x, y, text=self.translate[value], font=('Niagara Bold', self.scale_x - 40),
                                        tags=('text',))

    def start(self):
        self.root.mainloop()

    def reset(self):
        self.array = [[0] * self.size for _ in range(self.size)]
        self.canvas.delete('text')

    def move(self, r, c, bot=False):
        self.array[r][c] = self.turn + 1

        self.display()

        win, player = check_win(self.array, self.length, self.turn)
        if win:
            print(f'{player} won the game')
            exit()

        if all(all(row) for row in self.array):
            exit()

        self.turn = not self.turn

        if not (self.pvp or bot):
            r, c = self.bot.move()
            self.move(r, c, bot=True)


def check_win(array, length, turn):
    size = len(array)

    for row in array:
        for i, start in enumerate(row[:size - length + 1]):
            if start == 0:
                continue

            if len(set(row[i:i + length])) == 1:
                return True, (turn == start - 1)

    flat = list(chain.from_iterable(array))
    for step in (size, size + 1, size - 1):
        for i, start in enumerate(flat):
            if not start:
                continue
            for j in range(length - 1):
                if check_wrap(i, i + step, size):
                    break
                i += step
                if i >= len(flat) or flat[i] != start:
                    break
            else:
                return True, turn is bool(start - 1)

    return False, False


def check_wrap(x, x1, s):
    return abs(x // s - x1 // s) != 1


def tree_display(last):
    root = tkinter.Tk()
    root.geometry('1000x800')

    canv = tkinter.Canvas(root, width=1000, height=800)
    canv.pack()

    y = 0
    while True:
        upper = {}
        y += 100
        for i, node in enumerate(last):
            if node.prev not in upper:
                upper[node.prev] = [node]
            else:
                upper[node.prev].append(node)

            canv.create_text(i * 50, y, text=str(node.moves[-1]), font=('Niagara Bold', 5))

        last = list(upper.keys())
        if len(last) == 1:
            return root.mainloop()


if __name__ == '__main__':
    g = Game(5)
    g.start()
