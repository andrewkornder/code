class Minimax:
    def __init__(self, game, scoring, moves, depth):
        """

        :param game: the set of moves to get to the results game-state
        :param scoring: function that takes a set of moves, creates a board/game-state and returns a score from -1 to 1
        :param moves: a function that takes a set of moves and returns all legal moves from that position
        :param depth: how far to search
        """
        self.game, self.scoring, self.moves = game, scoring, moves
        self.depth = depth

    def get_move(self):
        tree = {0: [Node(None, self.game + [m]) for m in self.moves(self.game)]}
        for depth in range(1, self.depth):
            layer = []
            for node in tree[depth - 1]:
                if node.score not in (-1, 1):
                    layer.extend(self.branch(node))
            tree[depth] = layer

        # score the tree

    def branch(self, node):
        for move in self.moves(node.moves):
            child = node.child(move)
            child.score = self.scoring(child.moves)
        return node.next


class Node:
    def __init__(self, parent, move):
        self.score = 0
        self.next = []
        if parent is not None:
            self.moves = parent.moves + [move]

    def child(self, move):
        c = Node(self, move)
        self.next.append(c)
        return c