from chess_general import Piece


class Test(Piece):
    name = 'p'

    def __init__(self, board, r, c, color):
        super().__init__(board, r, c, color, self.name)

    def get_moves(self):
        return [(self.r + 1, self.c)]