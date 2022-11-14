from __future__ import annotations
from tkinter import PhotoImage


class Piece:
    @staticmethod
    def check_bounds(r, c):
        return 0 <= r < 8 and 0 <= c < 8

    @staticmethod
    def get_path(name, c):
        return f'../{"white" if c == 1 else "black"}{name}.png'

    def __init__(self, board, r, c, color, name, text=None):
        self.board, self.window = board, board.window
        self.r, self.c = r, c
        self.color = color

        self.image = PhotoImage(file=self.get_path(name, color))
        self.drawing = self.window.draw_image(r, c, self.image)
        self.text = text if text else name[0]
        if color == 1:
            self.text = self.text.upper()

    def open_square(self, r, c):
        p = self.board.arr[r][c]
        return p is None or p.color != self.color

    def move(self, r1, c1):
        self.board.arr[r1][c1] = self
        self.board.arr[self.r][self.c] = None
        self.r, self.c = r1, c1

        self.window.move_drawing(r1, c1, self.drawing)

    def get_special_moves(self): return []

    def __str__(self):
        return self.text

    @property
    def coords(self):
        return self.r, self.c


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

            p = self.board.arr[self.r - self.color][self.c + a]
            if p is not None and p.color != self.color:
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

    def get_special_moves(self):
        m = []
        if not self.can_castle:
            return m

        for c, dest in ((0, 2), (7, 6)):
            p = self.board.arr[self.r][c]
            if type(p) == Rook and p.can_castle:
                direction = -1 + 2 * (c > self.c)
                if all(self.board.arr[self.r][c1] is None for c1 in range(self.c + direction, c, direction)):
                    m.append((self.r, dest))

        return m

    def get_moves(self):
        m = []
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                if a == b == 0 or not (0 <= self.r + a < 8) or not (0 <= self.c + b < 8):
                    continue
                if self.open_square(self.r + a, self.c + b):
                    m.append((self.r + a, self.c + b))

        return m

    def move(self, r1, c1):
        self.can_castle = False
        Piece.move(self, r1, c1)

    def special_move(self, r1, c1):
        d = (c1 > self.c)
        rc = 7 * d
        Piece.move(self.board.arr[self.r][rc], self.r, c1 + 1 - 2 * (c1 > self.c))
        Piece.move(self, r1, c1)


class Knight(Piece):
    name = 'n'

    def __init__(self, board, r, c, color):
        super().__init__(board, r, c, color, self.name)

    def get_moves(self):
        m = []

        for a in (-2, 2):
            r1, c2 = self.r + a, self.c + a
            for b in (-1, 1):
                r2, c1 = self.r + b, self.c + b
                if self.check_bounds(r1, c1) and self.open_square(r1, c1):
                    m.append((r1, c1))
                if self.check_bounds(r2, c2) and self.open_square(r2, c2):
                    m.append((r2, c2))

        return m


class Bishop(Piece):
    name = 'b'

    def __init__(self, board, r, c, color):
        super().__init__(board, r, c, color, self.name)

    def get_moves(self: Bishop | Queen):
        m = []
        for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            r, c = self.r + dr, self.c + dc
            while True:
                if not self.check_bounds(r, c):
                    break

                p = self.board.arr[r][c]
                if p is not None:
                    if p.color != self.color:
                        m.append((r, c))
                    break
                m.append((r, c))
                r += dr
                c += dc

        return m


class Rook(Piece):
    name = 'r'

    def __init__(self, board, r, c, color):
        self.can_castle = True
        super().__init__(board, r, c, color, self.name)

    def get_moves(self: Rook | Queen):
        m = []

        for step in (-1, 1):
            r = self.r
            while True:
                r += step
                if not (0 <= r < 8):
                    break
                p = self.board.arr[r][self.c]
                if p is not None:
                    if p.color != self.color:
                        m.append((r, self.c))
                    break
                m.append((r, self.c))

        for step in (-1, 1):
            c = self.c
            while True:
                c += step
                if not (0 <= c < 8):
                    break
                p = self.board.arr[self.r][c]
                if p is not None:
                    if p.color != self.color:
                        m.append((self.r, c))
                    break
                m.append((self.r, c))

        return m

    def move(self, r1, c1):
        self.can_castle = False
        Piece.move(self, r1, c1)


class Queen(Piece):
    name = 'q'

    def __init__(self, board, r, c, color):
        super().__init__(board, r, c, color, self.name)

    def get_moves(self):
        return Bishop.get_moves(self) + Rook.get_moves(self)
