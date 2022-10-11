import random
import tkinter

background = '#eeeeee'
square = '#aaaaaa'
hover = '#999999'


def simulate(move, remove, value):
    game.board[move] = value
    r = game.check_gameover()
    if remove:
        game.board[move] = game.null

    return r


class Bot:
    @staticmethod
    def get_move():
        legal = [a for a in range(game.dim) if game.board[a] == game.null]
        value = [game.p1, game.p2][game.turn]
        next_value = [game.p1, game.p2][not game.turn]
        good_moves = []
        draws = []

        for move in legal[:]:
            if simulate(move, False, value):
                return move

            legal_b = [a for a in range(game.dim) if game.board[a] == game.null]

            r = [simulate(response, True, next_value) for response in legal_b]

            if not sum(r):
                good_moves.append(move)
            elif all([a == 2 for a in r]):
                draws.append(move)

            game.board[move] = game.null

        if len(good_moves):
            return random.choice(good_moves)
        elif len(draws):
            return random.choice(draws)

        print('cannot avoid losing')
        return random.choice(legal)

    def play(self):
        move = self.get_move()

        game.board[move] = [game.p1, game.p2][game.turn]
        game.display()

        gg = game.check_gameover()
        if gg:
            end_game(gg == 2)
            return

        game.turn = not game.turn


def xy_from_index(i, w, dx, dy):
    col = i % w
    row = (i - col) / w

    x, y = col * dx, row * dy

    return x, y, x + dx, y + dy


def horiz_vert():
    horiz = [list(range(width * a, width * a + width)) for a in range(height)]
    vert = [list(range(a, width * (height - 1) + a + 1, width)) for a in range(width)]

    return horiz, vert


class Grid:
    def __init__(self, size=(3, 3), values=('X', 'O', '')):
        self.banners = []

        self.dim = size[0] * size[1]
        self.p1, self.p2 = values[:2]
        self.null = values[2]

        self.board = [self.null for _ in range(self.dim)]
        self.turn = False
        self.waiting = True

        self.diagonals = self.get_diag()
        self.horizontals, self.verticals = horiz_vert()

        self.display()
        self.create_banner('START')

    def create_banner(self, text):
        a, b = dimX / 2, dimY / 2

        self.banners = [canvas.create_rectangle(0, 0, dimX, dimY, fill='#000000')]
        self.banners.append(canvas.create_text(a, b, text=text, font=('Niagara Solid', 60), fill='red'))

    def get_diag(self):
        return [list(range(0, self.dim, width + 1)), list(range(width - 1, width * (height - 1) + 1, width - 1))]

    def check_gameover(self):
        for point_list in [self.diagonals, self.horizontals, self.verticals]:
            for points in point_list:
                start = self.board[points[0]]
                if start == self.null:
                    continue
                if all([self.board[a] == start for a in points[1:]]):
                    return True
        if self.null not in self.board:
            return 2
        return False

    def display(self):
        canvas.delete('all')

        for i, val in enumerate(self.board):
            x, y, x1, y1 = xy_from_index(i, width, sx, sy)

            a, b = (x + x1) / 2, (y + y1) / 2

            canvas.create_rectangle(x, y, x1, y1, fill=square, activefill=hover)
            canvas.create_text(a, b, text=val, font=('Niagara Solid', 100))


def on_press(event):
    if game.waiting:
        game.waiting = False
        game.display()
        return

    x, y = int(event.y / sx), int(event.y / sy)
    i = y * width + x

    if game.board[i] != game.null:
        return

    game.board[i] = [game.p1, game.p2][game.turn]
    game.display()

    gg = game.check_gameover()
    if gg:
        end_game(gg == 2)
        return

    game.turn = not game.turn

    ai.play()


def rclick():
    if game.waiting and len(game.banners):
        for banner in game.banners:
            canvas.delete(banner)


def end_game(draw=False):
    text = 'DRAW' if draw else ('GAME OVER' if game.turn else 'YOU WIN')

    game.board = [game.null for _ in range(game.dim)]
    game.turn = False

    game.waiting = True
    game.create_banner(text)


if __name__ == '__main__':
    dimX = 600
    dimY = 600
    width = 3
    height = 3
    sx = dimX / width
    sy = dimY / height

    root = tkinter.Tk()
    root.title('')
    root.geometry(f'{dimX}x{dimY}')

    canvas = tkinter.Canvas(root, width=dimX, height=dimY, bg=background)
    canvas.pack()

    game = Grid((width, height))
    ai = Bot()

    canvas.bind('<Button-1>', on_press)
    canvas.bind('<Button-3>', lambda e: rclick())

    root.mainloop()
