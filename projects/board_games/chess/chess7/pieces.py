from chess_general import Piece


class Test(Piece):
    name = 'p'

    def __init__(self, board, r, c, color):
        super().__init__(board, r, c, color, self.name)

    def get_moves(self):
        return [(self.r + 1, self.c)]


class Pawn(Piece):
    name = 'p'

    def __init__(self, board, r, c, color):
        self.double_move = True
        super().__init__(board, r, c, color, self.name)

    def get_moves(self):
        m = []

        for i in range(1, 2 + self.double_move):
            # dont need to worry about out of bounds for r, since if it got the end, it would be promoted
            r = self.r - self.color * i
            if self.board.arr[r][self.c]:
                break
            m.append((r, self.c))

        for a in (-1, 1):
            if not (0 <= self.c + a < 8):
                continue

            if self.open_square(self.r - self.color, self.c + a):
                m.append((self.r - self.color, self.c + a))

        return m

    def move(self, r1, c1):
        self.double_move = False
        Piece.move(self, r1, c1)


class King(Piece):
    name = 'k'

    def __init__(self, board, r, c, color):
        self.can_castle = True
        super().__init__(board, r, c, color, self.name)

    def get_castle(self):
        # TODO: figure out castling mechanics and add it to the list
        return []

    def get_moves(self):
        m = []
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                if a == b == 0 or not (0 <= self.r + a < 8) or not (0 <= self.c + b < 8):
                    continue
                if self.open_square(self.r + a, self.c + b):
                    m.append((self.r + a, self.c + b))

        return m + self.get_castle()


class Knight(Piece):
    name = 'k'

    def __init__(self, board, r, c, color):
        super().__init__(board, r, c, color, self.name)

    def get_moves(self):
        m = []


class Bishop(Piece):
    name = 'b'

    def __init__(self, board, r, c, color):
        super().__init__(board, r, c, color, self.name)

    def get_moves(self):
        m = []


class Rook(Piece):
    name = 'r'

    def __init__(self, board, r, c, color):
        super().__init__(board, r, c, color, self.name)

    def get_moves(self):
        m = []


class Queen(Piece):
    name = 'q'

    def __init__(self, board, r, c, color):
        super().__init__(board, r, c, color, self.name)

    def get_moves(self):
        return Bishop.get_moves(self) + Rook.get_moves(self)
