import math
import tkinter


class Piece:
    def __init__(self, c, a, b):
        self.color = c
        self.fill = '#000000' if c == 'b' else '#ff0000'

        self.row = a
        self.col = b


def start():
    global board, circles, turn
    turn = 'r'
    board = [[], [], [], [], [], [], [], []]
    circles = [[], [], [], [], [], [], [], []]
    gui()

    board_colors = ['#dd3333', '#111111']
    for a in range(8):
        for b in range(8):
            x, y = b * 125, a * 125
            canvas.create_rectangle(x, y, x + 125, y + 125, fill=board_colors[(a + b) % 2], activefill='#FFEB3B')
            if (a + b) % 2 == 0 and not (2 < a < 5):
                if a < 3:
                    c = 'b'
                elif a > 4:
                    c = 'r'
                p = Piece(c, a, b)
                board[a].append(p)
                circles[a].append(canvas.create_oval(x + 22, y + 22, x + 102, y + 102, fill=p.fill))
            else:
                board[a].append(None)
                circles[a].append(None)

    global current_piece
    current_piece = board[0][0]

    root.mainloop()


def gui():
    global root
    root = tkinter.Tk()
    dim = 1200
    root.geometry('{0}x{0}'.format(dim))
    root.configure(background='black')

    global canvas, holding
    holding = None

    canvas = tkinter.Canvas(root, width=1000, height=1000, bg='black')

    canvas.bind('<ButtonPress>', select_piece)
    canvas.bind('<Motion>', update)
    canvas.bind('<ButtonRelease>', deselect)

    canvas.pack()


def check_legal(to, fro):
    tp = board[to[0]][to[1]]
    fp = board[fro[0]][fro[1]]

    long_cap = [False]

    if sum(to) % 2 != sum(fro) % 2:
        print('cannot move sideways or forward')
        return False, long_cap

    if math.dist(to, fro) > 1.415:
        print('too far, checking if legal')
        d = (1 - 2 * (to[0] > fro[0]), 1 - 2 * (to[1] > fro[1]))
        between = board[to[0] + d[0]][to[1] + d[1]]
        if tp is None:
            long_cap = [check_capture(fp, between), between]
        else:
            print(tp, '- failed')
            return False, long_cap

    if tp is not None:
        print('cannot take, not legal')
        return False, long_cap

    return True, long_cap


def check_capture(fro, bet):
    return not (bet is None or bet.color == fro.color)


def deselect(event):
    if current_piece == None:
        return None

    row, col = int(event.y / 125), int(event.y / 125)

    global holding, turn
    canvas.delete(holding)
    holding = None

    oldr, oldc = current_piece.row, current_piece.col
    legal = check_legal((row, col), (oldr, oldc))

    to = board[row][col]
    if legal[0] and (to is None or to.color != current_piece.color):
        turn = 'r' if turn == 'b' else 'b'
        board[row][col] = current_piece

        current_piece.row, current_piece.col = row, col

        if not legal[1][0]:
            board[oldr][oldc] = None
            canvas.delete(circles[row][col])
        else:
            r1, c1 = legal[1][1].row, legal[1][1].col
            board[r1][c1] = None
            canvas.delete(circles[r1][c1])

        cx, cy = col * 125 + 22, row * 125 + 22
        circles[row][col] = canvas.create_oval(cx, cy, cx + 80, cy + 80, fill=current_piece.fill)
        return None

    cx, cy = oldc * 125 + 22, oldr * 125 + 22
    circles[oldr][oldc] = canvas.create_oval(cx, cy, cx + 80, cy + 80, fill=current_piece.fill)


def select_piece(event):
    row, col = int(event.y / 125), int(event.y / 125)

    global current_piece
    current_piece = board[row][col]

    if current_piece is None:
        print('did not find a piece at:', row, col)
        return None
    elif current_piece.color != turn:
        print('wrong turn')
        current_piece = None
        return None

    global holding
    canvas.delete(circles[row][col])
    holding = canvas.create_oval(event.y - 40, event.y - 40, event.y + 40, event.y + 40, fill=current_piece.fill)


def update(event):
    global holding

    if holding is not None:
        canvas.delete(holding)
        holding = canvas.create_oval(event.y - 40, event.y - 40, event.y + 40, event.y + 40, fill=current_piece.fill)


if __name__ == '__main__':
    start()
