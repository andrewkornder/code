#!/usr/bin/python

from tkinter import Tk, Canvas, PhotoImage, CENTER
from typing import Any
from os import name
from stockfish import Stockfish

LIGHT = '#E8D3BB'
DARK = '#9A715E'
TEXT_COLOR = '#FFFFFF'
MOVE_COLOR = '#FF0000'
PLAYER_COLOR = True  # True => 'white', False => 'black'

WINDOWS = name == 'nt'

if WINDOWS:
    stockfish = Stockfish('./stockfish_15/stockfish.exe')
    stockfish.set_depth(15)

    stockfish.set_skill_level(20)
    current_elo = 20


class Board:
    def __init__(self, canvas: Canvas = None, height=None, width=None, pvp=False, display=__name__ == '__main__'):
        self.display = display
        self.pvp = pvp  # whether to play player vs player or player vs engine

        order = dict(zip(range(8), [
            Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
        ]))
        self.array = [
            [order[i]('black', self, (0, i)) for i in range(8)],
            [Pawn('black', self, (1, i)) for i in range(8)],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Pawn('white', self, (6, i)) for i in range(8)],
            [order[i]('white', self, (7, i)) for i in range(8)]
        ]
        self.check = {True: False, False: False}
        self.check_moves = []
        self.castle_moves = {}

        if display:
            if any(param is None for param in (canvas, height, width)):
                raise TypeError(
                    "Board.__init__() missing at least 1 positional argument")

            canvas.focus_force()

            bindings = {
                '<ButtonPress>': self.select,
                '<ButtonRelease>': self.release,
                '<Motion>': self.drag,
                '<Escape>': lambda e: self.help(),
                '<Key>': lambda e: print(self.text_display()) if e.keysym in '1234567890' else None,
                '<Return>': lambda e: self.swap_opponent(),
                '<c>': lambda e: stockfish.set_skill_level((current_elo - 1) if current_elo > 1 else 1)
            }

            for seq, func in bindings.items():
                canvas.bind(seq, func)

            self.canvas = canvas
            self.scaleX, self.scaleY = height // 8, width // 8
            self.starting_display()

        self.turn = True  # True if white's turn, False if black's turn
        self.selected = None
        self.selected_moves = []
        self.game_over = False

    @staticmethod
    def help():
        print("""Drag and drop => move piece
Space => alternate between playing the engine or the player
0-9 => show the results board position in text 
Return => Display key binds""")

    def swap_opponent(self):
        self.pvp = not self.pvp

    def _circle_coords(self, c, r):
        x, y = (c + 0.5) * self.scaleX, (r + 0.5) * self.scaleY
        sx, sy = self.scaleX // 5, self.scaleY // 5
        return x - sx, y - sy, x + sx, y + sy

    def _line_coords(self, c, r, c1, r1):
        x, y = (c + 0.5) * self.scaleX, (r + 0.5) * self.scaleY
        x1, y1 = (c1 + 0.5) * self.scaleX, (r1 + 0.5) * self.scaleY
        return x, y, x1, y1

    def _move_to_castle(self, *rc):
        if rc in self.castle_moves:
            return rc, self.castle_moves[rc]
        return False

    def starting_display(self):
        self.canvas.delete('all')
        for r, row in enumerate(self.array):
            y = self.scaleY * r
            for c, piece in enumerate(row):
                x = self.scaleX * c
                self.canvas.tag_lower(self.canvas.create_rectangle(
                    x, y, x + self.scaleX, y + self.scaleY,
                    fill=LIGHT if (r + c) % 2 else DARK))

                if piece is None:
                    continue

                piece.drawing = self.canvas.create_image(x + self.scaleX / 2, y + self.scaleY / 2, image=piece.image,
                                                         anchor=CENTER)

    def select(self, event):
        c, r = event.x // self.scaleX, event.y // self.scaleY
        self.selected = self.array[r][c]
        if self.selected is None:
            return
        if ['black', 'white'][self.turn] != self.selected.color:
            self.selected = None
            return

        if not self.check[self.turn]:
            self.selected_moves = self.selected.get_moves()
            if isinstance(self.selected, King):
                self.castle_moves = self.selected.can_castle()
            else:
                self.castle_moves = {}

            for r1, c1 in self.selected_moves + list(self.castle_moves.keys()):
                self.canvas.create_oval(*self._circle_coords(c1, r1),
                                        fill=MOVE_COLOR, tags=('move display',))
            self.canvas.tag_raise(self.selected.drawing)
        else:
            for p, (r1, c1) in self.check_moves:
                if p == (r, c):
                    self.canvas.create_oval(*self._circle_coords(c1, r1),
                                            fill=MOVE_COLOR, tags=('move display',))
            self.canvas.tag_raise(self.selected.drawing)

    def drag(self, event):
        if self.selected is None:
            return
        sx, sy = self.selected.image.height() / 2, self.selected.image.width() / 2
        self.canvas.moveto(self.selected.drawing, event.x - sx, event.y - sy)

    def release(self, event):
        piece = self.selected
        self.selected = None
        if piece is None:
            return
        self.canvas.delete('move display')

        c, r = event.x // self.scaleX, event.y // self.scaleY
        castling = self._move_to_castle(r, c)

        if not self.check[self.turn]:
            if (r, c) not in self.selected_moves and not castling:
                self.canvas.moveto(piece.drawing, piece.col *
                                   self.scaleX, piece.row * self.scaleY)
                return
        else:
            if ((piece.row, piece.col), (r, c)) not in self.check_moves:
                self.canvas.moveto(piece.drawing, piece.col *
                                   self.scaleX, piece.row * self.scaleY)
                return

            self.check[self.turn] = False

        if castling:
            k, (rp, rr, rc) = castling
            piece.move(k)
            rp.move((rr, rc))

        else:
            piece.move((r, c))
            if isinstance(piece, Pawn) and piece.row in (0, 7):
                piece.promote()

        if WINDOWS: stockfish.set_fen_position(self.get_fen())

        self.in_check()
        self.turn = not self.turn
        if self.check[self.turn]:
            self.out_of_check()
            if not self.check_moves:
                self.game_over = (True, self.turn)
                # TODO: do something on checkmate
                # TODO: method to restart game and then bind said method to a keypress

        if not self.pvp:
            if self.game_over:
                return
            move = stockfish.get_best_move(2000, 2000)
            stockfish.make_moves_from_current_position([move])

            # TODO: laugh at this laggy shitty coding because index didn't store the board well
            # redrawing the entire board bc why not
            self.from_fen(stockfish.get_fen_position())
            self.turn = not self.turn
            # piece, to = self.decode_algebraic(move)
            # piece.move(to)
            # r, c = to
            # self.canvas.moveto(piece.drawing, c * self.scaleX, r * self.scaleY)
        print(self.text_display())

    def decode_algebraic(self, notation):
        # ex: e2e4,
        #     g1f3
        c, r, c1, r1 = notation

        c, c1 = 'abcdefgh'.index(c), 'abcdefgh'.index(c1)
        r, r1 = 8 - int(r), 8 - int(r1)
        return self.array[r][c], (r1, c1)

    @staticmethod
    def encode_algebraic(piece, r1, c1):
        a = 'abcdefgh'[piece.col] + str(8 - piece.row)
        b = 'abcdefgh'[c1] + str(8 - r1)
        return a + b

    # only used to promote a pawn, where we need to redraw the image for the new piece
    def draw_image(self, piece):
        x, y = (piece.col + 0.5) * self.scaleX, (piece.row + 0.5) * self.scaleY
        return self.canvas.create_image(x, y, image=piece.image, anchor=CENTER)

    def in_check(self):
        self.check = {True: False, False: False}
        for i, row in enumerate(self.array):
            for j, p in enumerate(row):
                if p is None:
                    continue

                if any(isinstance(self.array[r][c], King) and
                       self.array[r][c].color != p.color for r, c in p.get_moves()):
                    self.check[p.color == 'black'] = True

    def check_move(self, piece, move):
        origin = (piece.row, piece.col)
        copy, check_copy = [a[:] for a in self.array], self.check.copy()

        piece.move(move, test=True)
        self.in_check()
        piece.move(origin, test=True)

        self.array = copy
        result = not self.check[self.turn]
        self.check = check_copy
        return result

    def out_of_check(self):
        self.check_moves = []
        for i, row in enumerate(self.array):
            for j, p in enumerate(row):
                if p is None:
                    continue
                if ['black', 'white'][self.turn] != p.color:
                    continue
                moves = p.get_moves()
                self.check_moves += [((p.row, p.col), m)
                                     for m in moves if self.check_move(p, m)]

    def text_display(self):
        rows = '+-----+-----+-----+-----+-----+-----+-----+-----+\n'
        cols = '  |  '

        string = rows[:]
        for i in range(16):
            if i % 2:
                string += rows
            else:
                string += '|  ' + cols.join(item.text if item else ' ' for item in self.array[i // 2]) + '  |' + '\n'
        return string

    def get_fen(self):
        fen = []
        for row in self.array:
            string = ''
            spacing = 0
            for item in row:
                if item is None:
                    spacing += 1
                    continue
                if spacing:
                    string += str(spacing)
                    spacing = 0
                string += item.text

            if spacing:
                string += str(spacing)
            fen.append(string)
        return '/'.join(fen)

    def from_fen(self, fen):
        text = {
            'p': Pawn,
            'r': Rook,
            'k': King,
            'n': Knight,
            'b': Bishop,
            'q': Queen
        }

        self.array = []
        for row, encoded in enumerate(fen.split('/')):
            self.array.append([])
            index = 0
            for char in encoded:
                if char == ' ':
                    break
                if char.isdigit():
                    self.array[-1] += [None] * int(char)
                    index += int(char)
                    continue

                color = 'black' if char.islower() else 'white'
                self.array[-1].append(text[char.lower()](color, self, (row, index)))
                index += 1

        if self.display:
            self.starting_display()


class Piece:
    text = ' '

    def __init__(self, color, board, pos):
        self.first_move = True
        self.color = color
        self.board = board
        self.row, self.col = pos
        self.drawing = None
        if board.display:
            self.image = PhotoImage(file=f'../{self.color}{self.text}.png')
        if self.color == 'white':
            self.text = self.text.upper()

    def move(self, to, test=False):
        self.board.array[self.row][self.col] = None
        self.row, self.col = to
        to_piece = self.board.array[self.row][self.col]

        if not test:
            if to_piece is not None and self.board.display:
                self.board.canvas.delete(to_piece.drawing)
            self.first_move = False
            self.board.canvas.moveto(self.drawing, self.col * self.board.scaleX, self.row * self.board.scaleY)

        self.board.array[self.row][self.col] = self

    def legal_moves(self, possible):
        moves = []
        for r, c in possible:
            if r == self.row and c == self.col:
                continue
            if 8 > r >= 0 and 8 > c >= 0:
                piece = self.board.array[r][c]
                if piece is None or piece.color != self.color:
                    moves.append((r, c))

        return moves


class Pawn(Piece):
    text = 'p'

    def __init__(self, color, board, pos):
        self.direction = 1 if color == 'black' else -1
        Piece.__init__(self, color, board, pos)

    def get_moves(self):
        legal = []

        row = self.row + self.direction
        if 8 > row >= 0 and self.board.array[row][self.col] is None:
            legal.append((row, self.col))
            if self.first_move:
                row += self.direction
                if 8 > row >= 0 and self.board.array[row][self.col] is None:
                    legal.append((row, self.col))

        row = self.row + self.direction
        if not (8 > row >= 0):
            return legal

        for i in (-1, 1):
            col = self.col + i
            if 8 > col >= 0:
                square = self.board.array[row][col]
                if square is not None and square.color != self.color:
                    legal.append((row, col))

        return legal

    def promote(self, cls=None):
        if cls is None:
            cls = Queen

        promoted = cls(self.color, self.board, (self.row, self.col))
        self.board.array[self.row][self.col] = promoted

        if self.board.display:
            self.board.canvas.delete(self.drawing)
            promoted.drawing = self.board.draw_image(promoted)

        del self


class King(Piece):
    text = 'k'

    def get_moves(self):
        # TODO: maybe disallow moving into check
        legal = [(self.row + r, self.col + c)
                 for r in (-1, 0, 1) for c in (-1, 0, 1)]

        moves = self.legal_moves(legal)

        return moves

    def can_castle(self):
        if not self.first_move:
            return []

        moves = {}
        row = self.board.array[self.row]
        left, right = False, False

        left_rook = row[0]
        right_rook = row[7]

        if isinstance(left_rook, Rook) and left_rook.first_move:
            left = all(x is None for x in row[1:4])
        if isinstance(right_rook, Rook) and right_rook.first_move:
            right = all(x is None for x in row[5:7])

        if left:
            moves[(self.row, 2)] = left_rook, self.row, 3
        if right:
            moves[(self.row, 6)] = right_rook, self.row, 5

        return moves


class Rook(Piece):
    text = 'r'

    def get_moves(self: Any):
        moves = []
        for d, s in ((8, 1), (-1, -1)):
            for r in range(self.row + s, d, s):
                piece = self.board.array[r][self.col]
                if piece is not None:
                    if piece.color != self.color:
                        moves.append((r, self.col))
                    break
                moves.append((r, self.col))
            for c in range(self.col + s, d, s):
                piece = self.board.array[self.row][c]
                if piece is not None:
                    if piece.color != self.color:
                        moves.append((self.row, c))
                    break
                moves.append((self.row, c))
        return self.legal_moves(moves)


class Knight(Piece):
    text = 'n'

    def get_moves(self):
        moves = []
        for m1 in (-2, 2):
            for m2 in (-1, 1):
                moves.append((self.row + m1, self.col + m2))
                moves.append((self.row + m2, self.col + m1))
        return self.legal_moves(moves)


class Bishop(Piece):
    text = 'b'

    def get_moves(self: Any):
        moves = []
        for rs, cs in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            r, c = self.row, self.col
            while True:
                r += rs
                c += cs
                if not (8 > r >= 0 and 8 > c >= 0):
                    break
                sq = self.board.array[r][c]
                if sq is not None:
                    if sq.color != self.color:
                        moves.append((r, c))
                    break
                moves.append((r, c))
        return moves


class Queen(Piece):
    text = 'q'

    def get_moves(self):
        return Bishop.get_moves(self) + Rook.get_moves(self)


def window():
    dim = 800

    root = Tk()
    root.geometry(f'{dim}x{dim}+10+10')

    canvas = Canvas(root, height=dim, width=dim)
    canvas.pack()

    Board(canvas, dim, dim, pvp=WINDOWS)

    return root.mainloop()


if __name__ == '__main__':
    window()
