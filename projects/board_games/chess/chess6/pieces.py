from tkinter import PhotoImage


def out_of_bounds(r, c):
    return not ((0 <= r < 8) and (0 <= c < 8))


class Piece:
    text = ''

    def __init__(self, game, color, loc):
        self.game = game
        self.color = color
        self.r, self.c = loc
        self.first_move = True

        if game.DISPLAY:
            file = 'black' if color == 'b' else 'white'
            self.image = PhotoImage(file=f'../code/projects/chess/{file}{self.text}.png')
            self.drawing = game.canvas.create_image(*game.canvas_location_center(*loc), image=self.image,
                                                    tags=('pieces',))
            self.height, self.width = self.image.height(), self.image.width()

        if self.color == 'w':
            self.text = self.text.upper()
    
    @property
    def array(self):
        return self.game.array

    @property
    def coords(self):
        return self.r, self.c
    
    def move(self, r, c):
        self.array[self.r][self.c] = None

        self.r, self.c = r, c
        take = self.array[r][c]

        self.array[r][c] = self

        if self.game.DISPLAY:
            if take is not None:
                self.game.canvas.delete(take.drawing)
            self.game.canvas.moveto(self.drawing, *self.game.canvas_location(r, c))
        self.first_move = False


class Pawn(Piece):
    text = 'p'
    
    def get_moves(self):
        m = -1 + 2 * (self.color == 'b')  # only piece where the piece had different moves depending on color
        moves = []

        for a in range(1, 2 + self.first_move):  # forward moves, 1 if the pawn has moved, or 2 if not
            r = self.r + a * m
            if not (0 <= r < 8):
                break
            if self.array[r][self.c] is not None:
                break
            moves.append((r, self.c))

        r = self.r + m
        if not (0 <= r < 8):
            return moves

        for a in (-1, 1):  # diagonal captures
            c = self.c + a
            if not (0 <= c < 8):
                continue
            if self.array[r][c] is not None and self.array[r][c].color != self.color:
                moves.append((r, c))

        return moves


class Rook(Piece):
    text = 'r'
    
    def get_moves(self):
        moves = []
        for rs, cs in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            r, c = self.r + rs, self.c + cs
            while True:
                if out_of_bounds(r, c):
                    break
                if self.array[r][c] is not None:
                    if self.array[r][c].color != self.color:
                        moves.append((r, c))
                    break
                moves.append((r, c))
                r += rs
                c += cs
        return moves


class Knight(Piece):
    text = 'n'
    
    def get_moves(self):
        moves = []
        for a in (-2, 2):
            r1, c2 = self.r + a, self.c + a
            for b in (-1, 1):
                c1, r2 = self.c + b, self.r + b
                if not out_of_bounds(r1, c1):
                    moves.append((r1, c1))
                if not out_of_bounds(r2, c2):
                    moves.append((r2, c2))
        
        legal = []
        for r, c in moves:
            if self.array[r][c] is None or self.array[r][c].color != self.color:
                legal.append((r, c))
        return legal


class Bishop(Piece):
    text = 'b'
    
    def get_moves(self):
        moves = []
        for rs, cs in ((1, 1), (-1, 1), (-1, 1), (-1, -1)):
            r, c = self.r + rs, self.c + cs
            while True:
                if out_of_bounds(r, c):
                    break
                if self.array[r][c] is not None:
                    if self.array[r][c].color != self.color:
                        moves.append((r, c))
                    break
                moves.append((r, c))
                r += rs
                c += cs
        return moves


class Queen(Piece):
    text = 'q'

    # no inspection because the functions .get_moves() for Rook and Bishop pieces dont like a queen object being passed
    # noinspection PyTypeChecker
    def get_moves(self):
        return list(set(Rook.get_moves(self) + Bishop.get_moves(self)))


class King(Piece):
    text = 'k'
    
    def get_moves(self):
        moves = [(self.r + a, self.c + b) for a in range(-1, 2) for b in range(-1, 2) if a | b]
        legal = []
        for r, c in moves:
            if out_of_bounds(r, c):
                continue
            if self.array[r][c] is None or self.array[r][c].color != self.color:
                legal.append((r, c))
        # TODO: castle and check
        return legal
    