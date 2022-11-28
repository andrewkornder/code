from itertools import chain
from tkinter import Tk, Canvas
from pprint import pprint


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
    def __init__(self, depth=4):
        self.length = None
        self.game = None
        self.size = None
        self.turn = None
        self.depth = depth

    @staticmethod
    def count_turn(board):
        return sum(sum(r) for r in board) % 2

    @staticmethod
    def reformat(board):
        return [[a + 1 for a in r] for r in board]

    def move(self, board):
        self.turn = self.count_turn(board.chosen)
        self.size = len(board)
        self.game = self.reformat(board)
        self.length = 3 if self.size == 3 else (4 if self.size == 5 else 5)
        return self.get_move()
    
    def get_move(self):
        if all(sum(row) == 0 for row in self.game):
            return self.size // 2, self.size // 2

        top = Node([], None)
        turn = self.turn

        layers = {}
        for depth in range(self.depth):
            layer = []
            for node in (layers[depth - 1] if layers else (top,)):
                if node.score == 0:
                    layer += self.branch(node, turn)
            layers[depth] = layer
            turn = not turn

        self.score_branches(layers, self.turn)

        top_layer = layers[0]
        pprint(layers)
        best = max(top_layer, key=lambda x: x.score).moves[-1]
        return best

    def score_branches(self, layers, turn):
        for depth in layers:
            layer = layers[depth]
            for node in layer:
                if node.children:
                    node.score = sum(x.score for x in node.children) / len(node.children)

    def branch(self, node, turn):
        copy = node.get_board(self.game, self.turn)
        for move in all_moves(copy):
            n = Node(node.moves + [move], node)
            c, p = self.check_win(n.get_board(self.game, self.turn), turn)
            n.score = c * (-1 + 2 * p)
            node.children.append(n)

        return node.children

    def check_win(self, array, turn, length=None, size=None):
        if length is None:
            length = self.length
        if size is None:
            size = self.size

        for row in array:
            for i, start in enumerate(row[:size - length + 1]):
                if start == 0:
                    continue

                if len(set(row[i:i + length])) == 1:
                    return True, -1 + 2 * turn

        flat = list(chain.from_iterable(array))
        for step in (size, size + 1, size - 1):
            for i, start in enumerate(flat):
                if not start:
                    continue
                for j in range(length - 1):
                    if self.check_wrap(i, i + step, size):
                        break
                    i += step
                    if i >= len(flat) or flat[i] != start:
                        break
                else:
                    return True, -1 + 2 * turn

        return False, False
# True, +- 1
# False, False

    @staticmethod
    def check_wrap(x, x1, s):
        return abs(x // s - x1 // s) != 1

    def move_old(self, game):
        self.game = game.array
        self.turn = game.turn
        self.length = 3 if self.size == 3 else (4 if self.size == 5 else 5)
        self.size = len(game.array)
        return self.get_move()


class Game:
    def __init__(self, size=3, length=3, window_size=(150, 150), text=(' ', 'x', 'o')):
        self.scale_x, self.scale_y = window_size
        self.win_width, self.win_height = self.scale_x * size, self.scale_y * size
        self.size = size

        self.root = Tk()
        self.root.geometry(f'{self.win_width}x{self.win_height}')

        self.canvas = Canvas(self.root, bg='white', height=self.win_height, width=self.win_width)
        self.canvas.pack()

        self.draw_lines(size)
        self.bindings()

        self.array = [[0] * size for _ in range(size)]
        self.translate = dict(zip(range(3), text, strict=True))
        self.reverse_trans = {v: k for k, v in self.translate.items()}

        self.turn = False

        self.bot = Bot()
        self.pvp = False

        self.length = 4

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

        win, player = self.bot.check_win(self.array, self.turn, length=self.length, size=self.size)
        if win:
            print(f'{player} won the game')
            exit()

        if all(all(row) for row in self.array):
            exit()

        self.turn = not self.turn

        if not (self.pvp or bot):
            r, c = self.bot.move_old(self)
            self.move(r, c, bot=True)


if __name__ == '__main__':
    Game(3).start()
