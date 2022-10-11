import tkinter


class chess_piece:
    def __init__(self, y=0, x=0, name=None):
        self.x = x
        self.y = y
        if name is None:
            allpieces[self.x].insert(self.y, self)
            self.name = \
            {0: 'r', 1: 'n', 2: 'b', 3: 'q', 4: 'k', 7: 'r', 6: 'n', 5: 'b'}[
                self.x] if self.y in [7, 0] else ' '
            if self.y in [1, 6]:
                self.name = 'p'
                self.double = True
            if self.y in [1, 0]:
                self.color = 'black'
            elif self.y in [6, 7]:
                self.color = 'white'
            else:
                self.color = 'grey'
        else:
            self.name = name
            self.color = 'grey'

        if self.name != ' ':
            self.file = tkinter.PhotoImage(file=self.color + self.name + '.png')
            self.img = None


def pawn(y, x, color, double_move):
    moves = []
    m = 1 if color == 'black' else -1
    moves.append((x, y + m * 1))
    moves.append((x + 1, y + m * 1))
    moves.append((x - 1, y + m * 1))
    if double_move:
        moves.append((x, y + m * 2))

    return [x for x in moves if max(x) < 9 and min(x) >= 0]


def knight(y, x):
    moves = []

    for a in [-1, 1]:
        for b in [2, -2]:
            c = x + b
            d = y + b
            moves += [(c, y + a), (x + a, d)]
    return [x for x in moves if max(x) < 8 and min(x) >= 0]


def rook(y, x):
    M = []
    M += [(x, i) for i in range(8)]
    M += [(i, y) for i in range(8)]
    M.remove((x, y))
    M.remove((x, y))
    return M


def to_notation(m):
    m[0] = 'abcdefgh'[m[0]]
    m[1] = 8 - m[1]
    return ''.join(map(str, m))


def start():
    global allpieces, turn
    turn = 'white'
    allpieces = [[], [], [], [], [], [], [], []]
    gui()

    board_colors = ['#2E7B54', '#AFBAB4']
    for j in range(8):
        for k in range(8):
            x, y = j * 125, k * 125
            canvas.create_rectangle(x, y, x + 125, y + 125,
                                    fill=board_colors[(k + j) % 2],
                                    activefill='#FFEB3B')
            chess_piece(j, k)

    global has_piece, current_piece
    has_piece = False
    current_piece = allpieces[0][0], 0, 0

    full_update(None)
    root.mainloop()


def gui():
    global root
    root = tkinter.Tk()
    dim = 1200
    root.geometry('{0}x{0}'.format(dim))
    root.configure(background='black')

    global canvas
    canvas = tkinter.Canvas(root, width=1000, height=1000, bg='black')

    canvas.bind('<ButtonPress>', select_piece)
    canvas.bind('<Motion>', update)
    canvas.bind('<ButtonRelease>', deselect_piece)

    canvas.pack()


def check_legal(piece1, piece2):
    if piece1.color == piece2.color or piece1.color != turn:
        return False

    if piece1.name == 'p':
        if (piece2.y, piece2.y) not in moves:
            return False
        if (piece2.y == piece1.y) ^ (piece2.name == ' '):
            return False
        piece1.double = False
    return (piece2.y, piece2.y) in moves


def capture(piece, x, y):
    piece1, piece2 = allpieces[piece[1]][piece[2]], allpieces[y][x]
    canvas.delete(current_piece[0].img)

    if not check_legal(piece1, piece2):
        piece1.img = canvas.create_image(piece1.x * 125 + 62,
                                         piece1.y * 125 + 62, image=piece1.file)
        return None
    del allpieces[piece[1]][piece[2]]
    if piece2.name != ' ':
        canvas.delete(piece2.img)

    piece1.img = canvas.create_image(y * 125 + 62, x * 125 + 62,
                                     image=piece1.file)
    allpieces[piece[1]].insert(piece[2], chess_piece(x, y, ' '))

    del allpieces[y][x]
    allpieces[y].insert(x, piece1)
    piece1.x = y
    piece1.y = x
    global turn
    turn = 'white' if turn == 'black' else 'black'


def deselect_piece(event):
    global has_piece, current_piece
    if has_piece:
        has_piece = False
        y, x = int(event.y / 125), int(event.y / 125)
        capture(current_piece, x, y)

        for poss_move in move_display:
            canvas.delete(poss_move)


def select_piece(event):
    update(event)
    global has_piece, current_piece
    has_piece = True
    y, x = int(event.y / 125), int(event.y / 125)
    if allpieces[y][x].name == ' ':
        has_piece = False
        return None
    current_piece = allpieces[y][x], y, x

    global move_display, moves
    moves = []
    if current_piece[0].name == 'p':
        moves = pawn(x, y, current_piece[0].color, current_piece[0].double)
    else:
        moves = {'n': knight, 'r': rook}[current_piece[0].name](x, y)
    move_display = []
    print([to_notation(list(m)) for m in moves])
    for m in moves:
        mx, my = m[0] * 125 + 62, m[1] * 125 + 62
        move_display.append(
            canvas.create_oval(mx - 15, my - 15, mx + 15, my + 15, fill='grey'))


def print_display():
    for n in range(len(allpieces)):
        for piece in allpieces[7 - n]:
            print(piece.name, end=' ')
        print('    ', n)
    print('\n' + ' '.join(map(str, range(8))))


def full_update(event):
    for i, row in enumerate(allpieces):
        for j, piece in enumerate(row):
            x, y = i * 125 + 62, j * 125 + 62
            if piece.name != ' ':
                piece.img = canvas.create_image(x + 50, y + 50,
                                                anchor=tkinter.SE,
                                                image=piece.file)


def update(event):
    if has_piece:
        cp = current_piece[0]
        canvas.delete(cp.img)
        cp.img = canvas.create_image(event.y, event.y, image=cp.file)


if __name__ == '__main__':
    start()
