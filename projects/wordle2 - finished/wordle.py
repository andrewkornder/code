import tkinter
import random
import scorekeeper as sk
from bot import test, remove_words

global guesses, answer_list, target, user


class Keyboard:
    def __init__(self):
        self.keys = {a: 'white' for a in 'qwertyuiop0asdfghjkl1zxcvbnm'}
        self.used = 'dark grey'
        self.image = tkinter.PhotoImage(file='backspace.png')
        self.update([], [])

    def reset(self):
        self.keys = {a: 'white' for a in 'qwertyuiop0asdfghjkl1zxcvbnm'}
        self.update([], [])

    def update(self, info, keys):
        key_display.delete('all')
        for key, result in zip(keys, info):
            self.keys[key] = result if result != 'grey' else self.used

        y, y1 = 0, 50
        offset = 0
        for i, (k, c) in enumerate(self.keys.items()):
            if k.isdigit():
                y, y1 = y + 50, y1 + 50
                offset = 11 if offset == 0 else 20
                continue

            x = (i - offset) * 50 + (25 if 9 < i < 20 else 0)
            x1 = x + 50
            key_display.create_rectangle(x, y, x1, y1, fill=c)
            key_display.create_text(x + 25, y + 25, text=k.upper())
        key_display.create_rectangle(400, 100, 450, 150, fill='white')
        key_display.create_image(425, 125, image=self.image)


class Grid:
    def __init__(self):
        self.row = 0
        self.arr = []
        self.reset()

    def reset(self):
        self.row = 0
        self.arr = [['white' for _ in range(5)] for _ in range(6)]

        canvas.delete('all')
        for i, row in enumerate(self.arr):
            y = 100 * i
            y1 = y + 100
            for j, item in enumerate(row):
                x = 100 * j
                x1 = x + 100
                canvas.create_rectangle(x, y, x1, y1, fill=item)

    def display(self, guess):
        guess += ' ' * (5 - len(guess))
        y = 100 * game.row
        y1 = y + 100
        guess = guess.upper()
        for j, item in enumerate(self.arr[game.row]):
            x = 100 * j
            x1 = x + 100
            canvas.create_rectangle(x, y, x1, y1, fill=item)
            canvas.create_text((x + x1) / 2, (y + y1) / 2, text=guess[j],
                               font=('Niagara Solid', 40))


def get_guess():
    global user, new_game, target

    if new_game:
        new_game = False
        target = random.choice(answer_list)
        game.reset()
        keyboard.reset()
        return

    if len(user) != 5:
        print('too short')
        return

    if user not in guesses:
        print(f'{user} was not found in guesses')
        return

    info = score(user, target)
    cinfo = [{'b': 'grey', 'g': 'green', 'y': 'yellow'}[i] for i in info]
    game.arr[game.row] = cinfo
    if all(i == 'g' for i in info):
        game.display(user.upper())
        sk.add_score(score_file, game.row, 5)
        new_game = True

    game.display(user.upper())
    keyboard.update(cinfo, user)

    game.row += 1
    if game.row == 7:
        new_game = True

    user = ''


def score(guess, ans):
    info = ['b'] * 5
    word, answer = list(guess), list(ans)

    for i, e in enumerate(word):
        if e == answer[i]:
            info[i] = 'g'
            answer[i] = ' '

    for i, e in enumerate(word):
        if info[i] != 'b':
            continue

        if e in answer:
            info[i] = 'y'
            answer[answer.index(e)] = ' '

    return info


def start_game():
    global guesses, answer_list, target, user
    with open('answers.txt', 'r') as a, open('guesses.txt', 'r') as g:
        answer_list = a.read().split('\n')
        guesses = g.read().split('\n') + answer_list

    target = random.choice(answer_list)
    user = ''


def key_press(k):
    global user

    if k not in 'abcdefghijklmnopqrstuvwxyz' or len(user) == 5:
        if k == 'BackSpace':
            user = user[:-1]
            game.display(user)
        return

    user += k
    game.display(user)


def window():
    global root, input_box, canvas, game, key_display, keyboard, new_game, score_file
    score_file = 'scores.txt'

    new_game = False

    root = tkinter.Tk()
    root.title('wordle clone')

    root.geometry('{}x{}'.format(500, 800))
    canvas = tkinter.Canvas(root, width=500, height=600, bg='white')
    canvas.grid(row=0, column=0)

    root.bind('<KeyPress>', lambda k: key_press(k.keysym))
    root.bind('<Return>', lambda e: get_guess())
    root.bind('<Escape>', lambda e: print(target))
    root.bind('<space>', lambda e: sk.show_scores_GUI(score_file))

    game = Grid()
    key_display = tkinter.Canvas(root, width=500, height=200, bg='white')
    key_display.grid(row=1, column=0)
    keyboard = Keyboard()

    start_game()

    root.mainloop()


def bot_play():
    target = random.choice(answer_list)
    l = answer_list[:]
    best = 'salet'
    while best != target:
        print(best, end=' ')
        info = score(best, target)
        cinfo = [{'b': 'grey', 'g': 'green', 'y': 'yellow'}[i] for i in info]

        game.arr[game.row] = cinfo
        game.display(best.upper())

        keyboard.update(cinfo, best)

        game.row += 1
        l = remove_words(best, info, l)
        l = test(l)
        best = l[0]
    print(target)
    game.reset()
    keyboard.reset()
    root.after(10, bot_play)


if __name__ == '__main__':
    window()
