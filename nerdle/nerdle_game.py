from random import choice
from tkinter import Tk, Canvas


class VisualKeyboard:
    def __init__(self, colors, keys, font, row_width, padding, parent, width, height, grid):
        self.colors = colors
        self.keys = keys
        self.values = {key: 'white' for key in self.keys}

        self.canvas = Canvas(parent, width=width, height=height)
        self.canvas.grid(**grid)

        self.rows = (lambda f: f if f.is_integer() else int(f) + 1)(len(keys) / row_width)

        self.padding = padding
        self.row_width = row_width
        self.key_width = (width - 2 * self.padding) / row_width
        self.key_height = height / self.rows

        self.center = width / 2
        for row in range(self.rows):
            y = row * self.key_height
            k = keys[row * row_width: (row + 1) * row_width]
            for c, key in enumerate(k):
                x = self.center + (c - len(k) / 2) * self.key_width
                self.canvas.create_rectangle(x, y, x + self.key_width, y + self.key_height,
                                             fill='white', outline='black', tags=('colors',))
                self.canvas.create_text(x + self.key_width / 2, y + self.key_height / 2,
                                        fill='black', text=key, tags=('text',), font=font)

    def update(self, guess, score):
        d = dict(zip(guess, score))
        for row in range(self.rows):
            y = row * self.key_height
            k = self.keys[row * self.row_width: (row + 1) * self.row_width]
            for c, key in enumerate(k):
                if key not in guess:
                    continue
                x = self.center + (c - len(k) / 2) * self.key_width
                self.canvas.create_rectangle(x, y, x + self.key_width, y + self.key_height,
                                             fill=self.colors[d[key]], outline='black', tags=('colors',))
        self.canvas.tag_raise('text')

    def reset(self):
        self.values = {key: 'white' for key in self.keys}


class Game:
    padding = 20
    kb_frac = .25

    def __init__(self, wordset, charset, rows, display=False, **kwargs):
        self.run = None
        self.keyboard_display = None
        self.canvas = None
        self.colors = None
        self.font = None
        self.root = None
        self.row_height = None
        self.canv_w = None
        self.box_size = None
        self.canv_h = None
        self.win_h = None
        self.win_w = None

        self.length = len(wordset[0])
        assert all(len(word) == self.length for word in wordset)

        self.words, self.chars = wordset, charset

        self.rows = rows

        self._game_state = [['' for _ in range(self.length)] for _ in range(rows)]
        self._scoring_state = [[-1] * self.length for _ in range(rows)]

        self.current_row = 0
        self.current_col = 0

        self.answer = list(choice(self.words))

        if display:
            self.create_window(**kwargs)

    def create_window(self, width, height, colors=('grey', 'yellow', 'green', 'white')):
        self.win_w, self.win_h = width, height
        self.canv_w, self.canv_h = width - 2 * self.padding, height * (1 - self.kb_frac)

        self.box_size = self.canv_w / self.length
        self.row_height = self.canv_h / self.rows

        self.root = Tk()
        self.root.geometry(f'{width}x{height}')

        self.font = ('Niagara Bold', self.canv_w // 20)
        self.colors = colors

        self.canvas = Canvas(self.root, width=self.win_w, height=self.canv_h)
        self.canvas.grid(row=0, column=0)

        self.keyboard_display = VisualKeyboard(
            colors, keys=self.chars, font=self.font, row_width=10, padding=self.padding,
            parent=self.root, width=self.win_w, height=self.win_h - self.canv_h, grid={'row': 1, 'column': 0}
        )

        self._set_binds()
        self.run = self.root.mainloop

        self.draw_game()

    def _set_binds(self):
        binds = [
            (self.root, 'Key', lambda event: self.add_char(event.keysym)),
            (self.root, 'Return', lambda _: self.check_guess()),
            (self.root, 'slash', lambda _: print('answer:', ''.join(self.answer))),
        ]
        for target, seq, func in binds:
            target.bind(f'<{seq}>', func)

    def add_char(self, character):
        print(character)

        if character not in self.chars or self.current_col == self.length:
            return

        self.active_row[self.current_col] = character
        self.current_col += 1

        self.draw_game(self.current_row)

    def draw_game(self, starting_row=None, ending_row=None):
        if ending_row is None:
            ending_row = starting_row + 1 if starting_row is not None else self.rows
        if starting_row is None:
            starting_row = 0

        y = starting_row * self.row_height
        for row in range(starting_row, ending_row):
            y1, x = y + self.row_height, self.padding
            game, score = self._game_state[row], self._scoring_state[row]
            for col in range(self.length):
                x1 = x + self.box_size
                self.canvas.create_rectangle(x, y, x1, y1, fill=self.colors[score[col]], outline='black')
                self.canvas.create_text((x + x1) / 2, (y + y1) / 2, text=game[col], fill='black', font=self.font)
                x = x1
            y = y1

    def check_guess(self):
        info = [0] * self.length
        word, answer = self.active_row, self.answer[:]

        for i, e in enumerate(word):
            if e == answer[i]:
                info[i] = 2
                answer[i] = ' '

        if all(x == 2 for x in info):
            self.end_game()

        for i, e in enumerate(word):
            if info[i] != 0:
                continue

            if e in answer:
                info[i] = 1
                answer[answer.index(e)] = ' '

        self._scoring_state[self.current_row] = info
        self.draw_game(self.current_row)

        self.current_row += 1
        self.current_col = 0

    @property
    def active_row(self):
        return self._game_state[self.current_row]

    @active_row.setter
    def active_row(self, row):
        assert len(row) == len(self.active_row)
        self._game_state[self.current_row] = row

    @property
    def guess(self):
        return self.state[self.current_row]

    @guess.setter
    def guess(self, guess: str):
        assert 0 <= len(guess) <= self.length
        self.active_row = list(guess)

        if len(guess) == self.length:
            self.check_guess()
        else:
            self.current_col = sum(bool(string) for string in self.active_row)

    @property
    def score(self):
        return self._scoring_state[self.current_row]

    @property
    def state(self):
        return self._game_state, self._scoring_state

    @state.setter
    def state(self, value: tuple[list, list]):
        game, score = value

        assert all(len(row) == self.length for row in game)
        assert len(game) == self.rows

        self.current_row = sum(all(row) for row in game)  # counts how many rows are not ['', '', ... , '', '']
        if self.current_row == self.rows:
            self.end_game()
            return

        self._game_state = game
        self._scoring_state = score
        self.current_col = sum(char != '' for char in self.active_row)

        self.draw_game()

    def text_state(self):
        return '\n'.join(''.join(self._game_state[row]) + ' | ' +
                         ''.join(map(lambda n: str(n) if n > 0 else ' ', self._scoring_state[row]))
                         for row in range(self.rows))

    def end_game(self):
        pass


class WordleBot:
    def __init__(self):
        # define sets or make generators of some sort for them
        self.wordset = []
        self.charset = []
        self.lives = 3
        # ** do something **

        self.game = Game(self.wordset, self.charset, self.lives)
        self.score = 0

    def get_guess(self):
        state = self.game.state
        print('\n'.join(map(lambda a: '\n'.join(map(''.join, a)), state)))

        guess = None
        # ** do something **
        self.game.guess(guess)
        self.score += sum(self.game.score)  # ????


if __name__ == '__main__':
    _w = ['array', 'crane', 'camps']
    _c = list('abcdefghijklmnopqrstuvwxyz')

    g = Game(_w, _c, 6, display=True, width=500, height=800)
    g.run()
