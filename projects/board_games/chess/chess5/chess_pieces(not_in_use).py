from tkinter import PhotoImage

DISPLAYING = True


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
            self.drawing = self.board.canvas.create_image(*get_canvas_loc(row, col), image=self.img, tags=('piece',))
        
        self.moves = []    
        self.get_moves()
    
    def move(self, *to, test=False):
        self.first_move = False
        
        self.board.array[self.row][self.col] = None
        self.row, self.col = to
        destination = self.board.array[self.row][self.col]
        self.board.array[self.row][self.col] = self
        
        if not test:
            if DISPLAYING:
                self.board.canvas.moveto(self.drawing, *get_canvas_loc(*to))
                
                if destination is not None:
                    self.board.canvas.delete(destination.drawing)
            self.get_moves()

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
        self.moves = m
    

class King(Piece):
    text = 'k'
    
    def get_moves(self):
        return self._check_moves((self.row + r, self.col + c) for r in (-1, 0, 1) for c in (-1, 0, 1))
    
        
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
        return list(set(Rook.get_moves(self) + Bishop.get_moves(self)))
        