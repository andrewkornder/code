import pprint
from itertools import chain
from functools import cache


class Node:
    def __init__(self, previous, move, legal):
        self.move = move
        self.legal = legal
        self.previous = previous
        self.score = 0
        self.next = []

    def child(self, move):
        legal = self.legal[:]
        legal.remove(move)

        n = Node(self, move, legal)
        self.next.append(n)
        return n

    def moves(self):
        if self.previous.previous is None:
            return self.move,
        return self.previous.moves() + (self.move,)

    def get_score(self, func):
        if self.next:
            self.score = func(a.score for a in self.next)

    def __repr__(self):
        return f'{self.move} -> {self.score}'


class Bot1:
    def __init__(self):
        self.length = None
        self.depth = None
        self.board = None
        self.legal = None
        self.turn = None
        self.size = None

    def move(self, board, depth=None):
        self.size = len(board.chosen)
        self.length = self.size  # TODO
        self.turn = sum(sum(r) for r in board.chosen) % 2
        self.legal = [(a, b) for a in range(self.size) for b in range(self.size) if not board.chosen[a][b]]

        self.board = board.the_grid

        self.depth = depth if depth is not None else self.size
        return self.get_move()

    def get_move(self):
        tree = {-1: [Node(None, None, self.legal)]}

        for depth in range(self.depth):
            layer = []
            for node in tree[depth - 1]:
                if not node.score:
                    layer.extend(self.branch(node))

            tree[depth] = layer

        tree = self.get_top_move(tree)
        top = tree[1]
        return min(top, key=lambda x: x.score).move

    def branch(self, node):
        for move in node.legal:
            n = node.child(move)
            n.score = check_win(n.moves(), self.length, self.size)
        return node.next

    def get_top_move(self, tree):
        for depth in range(1, self.depth):
            func = max if not depth % 2 else min
            for node in tree[depth]:
                node.get_score(func)
        pprint.pprint(tree)
        return tree


@cache
def check_win(moves, length, size):
    def check_wrap(x, x1, s):
        return x // s - x1 // s != 1

    def construct(m):
        board = [[-1] * size for _ in range(size)]
        t = True
        for a, b in m:
            board[a][b] = t
            t = not t
        return board

    array = construct(moves)

    for row in array:
        for i, start in enumerate(row[:size - length + 1]):
            if start == -1:
                continue

            if len(set(row[i:i + length])) == 1:
                return -1 + 2 * start

    flat = list(chain.from_iterable(array))
    gsize = len(flat)
    for step in (size, size + 1, size - 1):
        for i, start in enumerate(flat):
            if not start:
                continue
            for j in range(length - 1):
                i += step
                if check_wrap(i - step, i, size) or i >= gsize or flat[i] != start:
                    break
            else:
                return -1 + 2 * start

    return 0
