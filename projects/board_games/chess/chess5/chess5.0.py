from tkinter import PhotoImage, NW
import window

# TODO:
"""
get all working classes
check, checkmate
stockfish/bot
full display
efficiency
good interface with stockfish, and storage for moves
"""

LIGHT = '#E8D3BB'
DARK = '#9A715E'
DISPLAYING = True
win_x, win_y = 800, 800
scale_x, scale_y = win_x // 8, win_y // 8
circ_x, circ_y = scale_x // 4, scale_y // 4


class Piece:
    text = '_'

    def __init__(self, row, col, color, board):
        self.row, self.col = row, col
        self.first_move = True
        self.color = color
        self.board = board
        self.img = PhotoImage(file=f'../{color}{self.text}.png')

        if self.color == 'white':
            self.text = self.text.upper()

        if DISPLAYING:
            self.drawing = self.board.canvas.create_image(*get_canvas_loc(row, col), image=self.img, tags=('piece',),
                                                          anchor=NW)

        self.moves = []

    def move(self, *to, test=False):
        self.first_move = False

        self.board.array[self.row][self.col] = None
        self.row, self.col = to
        destination = self.board.array[self.row][self.col]
        self.board.array[self.row][self.col] = self

        if DISPLAYING and not test:
            self.board.canvas.moveto(self.drawing, *get_canvas_loc(*to))

            if destination is not None:
                self.board.canvas.delete(destination.drawing)

    def _check_moves(self, m):
        m2 = []
        for move in m:
            r, c = move
            if not (8 > r >= 0 and 8 > c >= 0):
                continue
            p = self.board.array[r][c]
            if p is None or p.color != self.color:
                m2.append(move)
        return m2


class Pawn(Piece):
    text = 'p'

    def __init__(self, row, col, color, board):
        self.mult = 1 if color == 'black' else -1
        Piece.__init__(self, row, col, color, board)

    def get_moves(self):
        self.moves = []
        for add in range(1, 2 + self.first_move):
            r = self.row + add * self.mult
            if self.board.array[r][self.col] is not None:
                break
            self.moves.append((r, self.col))

        r = self.row + self.mult
        for add in (-1, 1):
            c = self.col + add
            if not (8 < c <= 0):
                continue
            piece = self.board.array[r][c]
            if piece is not None and piece.color != self.color:
                self.moves.append((r, c))


class King(Piece):
    text = 'k'
    
    def castle(self):
        if not self.first_move:
            return []

    def get_moves(self):
        return self.castle() + self._check_moves((self.row + r, self.col + c) for r in (-1, 0, 1) for c in (-1, 0, 1))


class Knight(Piece):
    text = 'n'

    def get_moves(self):
        self.moves = []
        for a in (2, -2):
            r1, c1 = self.row + a, self.col + a
            for b in (-1, 1):
                r2, c2 = self.row + b, self.col + b
                self.moves.append((r1, c2))
                self.moves.append((r2, c1))
        self.moves = self._check_moves(self.moves)


class Bishop(Piece):
    text = 'b'

    def get_moves(self):
        self.moves = []

        for rs, cs in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            r, c = self.row + rs, self.col + cs
            while True:
                if not (8 > r >= 0 and 8 > c >= 0):
                    break
                p = self.board.array[r][c]
                if p is not None:
                    if p.color != self.color:
                        self.moves.append((r, c))
                    break
                self.moves.append((r, c))
                r += rs
                c += cs


class Rook(Piece):
    text = 'r'

    def get_moves(self):
        """so much code this time, :(
        it should be a tiny tiny bit faster though, since i'm only incrementing the stuff i really need
        but it's twice as long"""

        self.moves = []

        row = self.board.array[self.row]
        for cs in (1, -1):
            c = self.col + cs
            while True:
                if not (8 > c >= 0):
                    break
                p = row[c]
                if p is not None:
                    if p.color != self.color:
                        self.moves.append((self.row, c))
                    break
                self.moves.append((self.row, c))
                c += cs

        for rs in (1, -1):
            r = self.row + cs
            while True:
                if not (8 > r >= 0):
                    break
                p = self.board.array[r][self.col]
                if p is not None:
                    if p.color != self.color:
                        self.moves.append((r, self.col))
                    break
                self.moves.append((self.row, c))
                r += rs


class Queen(Piece):
    text = 'q'

    def get_moves(self):
        Rook.get_moves(self)
        m = self.moves[:]
        Bishop.get_moves(self)
        self.moves += m


def from_notation(text):
    """format => e2e4, g1f3
       return => (from_row, from_col), (to_row, to_col)
    """
    if len(text) == 2:
        fc, fr, tc, tr = text
        fr, tr = 8 - int(fr), 8 - int(tr)
        fc, tc = int(fc, base=18) - 10, int(tc, base=18) - 10
        return (fr, fc), (tr, tc)

    else:
        raise Exception(f'{text} wasn\'t in the right format for notation -> (row, col) conversion')


def to_notation(piece, to):
    """format => King() object at (2, 5), (2, 4)
       return => f4e4"""
    r, c = str(8 - piece.row), 'abcdefgh'[piece.col]
    r1, c1 = str(8 - to[0]), 'abcdefgh'[to[1]]

    return c + r + c1 + r1


def get_canvas_loc(row, col):
    return col * scale_x, row * scale_y

def get_canvas_circle(row, col):
    x, y = (col + 0.5) * scale_x, (row + 0.5) * scale_y
    return x - circ_x, y - circ_y, x + circ_x, y + circ_y

def show_text_display(board):
    rowsep = '+-----' * 8 + '+'
    colsep = '|'
    for row in board:
        print(rowsep)
        print(colsep + colsep.join(p.training_material.center(5, ' ') if p else '     ' for p in row) + colsep)

    print(rowsep)


class Board:
    order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    def __init__(self, canvas):
        self.canvas = canvas
        self.binds()

        self.array = [
            [self.order[i](0, i, 'black', self) for i in range(8)],
            [Pawn(1, i, 'black', self) for i in range(8)],
            *[[None] * 8 for _ in range(4)],
            [Pawn(6, i, 'white', self) for i in range(8)],
            [self.order[i](7, i, 'white', self) for i in range(8)]]

        self.turn = True
        self.check = False
        self.piece = None

        self.create_display()
        for row in self.array:
            for p in row:
                if p is not None:
                    p.get_moves()

    def binds(self):
        to_bind = [(self.canvas, 'Motion', self.drag),
                   (self.canvas, 'ButtonPress', self.press),
                   (self.canvas, 'ButtonRelease', self.release),
                   (self.canvas, 'space', lambda _: self.reset)]
        for item, seq, func in to_bind:
            item.bind(f'<{seq}>', func)

    def create_display(self):
        # all the piece images are created when initializing the piece themselves in Piece.__init__
        # all i have to do here is raise them above the squares
        for r, row in enumerate(self.array):
            y = scale_y * r
            for c, piece in enumerate(row):
                x = scale_x * c
                color = DARK if (r + c) % 2 else LIGHT
                self.canvas.create_rectangle(x, y, x + scale_x, y + scale_y, fill=color, tags=('squares',))
        self.canvas.tag_lower('squares')

    def press(self, event):
        row, col = event.y // scale_y, event.y // scale_x
        p = self.array[row][col]
        if p is None or (p.color == 'black') is self.turn:
            print('wrong color or empty square')
            return
        self.piece = p
        
        p.get_moves()
        for move in p.moves:
            print(to_notation(p, move))
            self.canvas.create_oval(*get_canvas_circle(*move), tags=('moves',), fill='red')
        self.canvas.tag_raise(p.drawing)

    def drag(self, event):
        if self.piece is None:
            return
        # hacky since the image size might/should change when window size does
        self.canvas.moveto(self.piece.drawing, event.y - 50, event.y - 50)

    def release(self, event):
        if self.piece is None:
            return
        
        self.canvas.delete('moves')
        row, col = event.y // scale_y, event.y // scale_x
        if (row, col) not in self.piece.moves:
            self.canvas.moveto(self.piece.drawing, *get_canvas_loc(self.piece.row, self.piece.col))
            self.piece = None
            return

        self.piece.move(row, col)
        self.piece = None
        
        self.turn = not self.turn


if __name__ == '__main__':
    app = window.App((win_x, win_y))
    Board(app.canvas)
    app.run()
