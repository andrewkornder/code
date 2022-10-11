from random import sample
import tkinter

SIZE = 10
BOMBS = 20
TILE_SIZE = 50

game_board = []


class Tile:
    def __init__(self, loc, bomb_list):
        self.loc = loc
        self.number = 0
        self.bomb = loc in bomb_list
        self.check_neighbors(bomb_list)

    def check_neighbors(self, arr):
        neighbors = [
            -SIZE - 1, -SIZE, -SIZE + 1,
            1, -1,
            SIZE + 1, SIZE, SIZE - 1
        ]

        for inc in neighbors:
            index = self.loc + inc
            if 0 <= index < SIZE ** 2:
                self.number += index in arr

    def __repr__(self):
        return f'{self.loc} {self.bomb} {self.number}'


def display(canv):
    for i, item in enumerate(game_board):
        x, y = (i % SIZE) * TILE_SIZE, (i // SIZE) * TILE_SIZE
        x1, y1 = x + TILE_SIZE, y + TILE_SIZE

        canv.create_rectangle(x + 2, y + 2, x1 - 2, y1 - 2, fill='white')

        x2, y2 = (x + x1) / 2, (y + y1) / 2
        canv.create_text(x2, y2, text=str(item.number))


def create_bombs():
    return sample(range(SIZE ** 2), BOMBS)


def create_game():
    root = tkinter.Tk()
    root.geometry('500x500')
    canvas = tkinter.Canvas(root, height=500, width=500, bg='grey')
    canvas.pack()

    bombs = create_bombs()
    for i in range(SIZE ** 2):
        game_board.append(Tile(i, bomb_list=bombs))
    print(game_board)
    display(canvas)

    root.bind('<Button-1>', lambda e: None)
    root.mainloop()


if __name__ == '__main__':
    create_game()
