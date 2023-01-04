from tkinter import Tk, Canvas, Entry, END
from random import randint, choice
from time import sleep


class Window:
    def __init__(self, w=800, h=800, uppercase=False):
        self.is_lower = not uppercase
        self.coords = w / 2, h / 2
        self.coords2 = w / 2, h / 2 - 100
        self.font = ('Niagara Bold', 100)
        self.font2 = ('Niagara Bold', 50)

        self.root = Tk()
        self.root.geometry(f'{w}x{h + 100}')
        self.root.bind('<Return>', self.check)

        self.canvas = Canvas(self.root, width=w, height=h)
        self.canvas.grid(row=0, column=0)

        self.input = Entry(self.root)
        self.input.grid(row=1, column=0)

        self.answer = 'alpha'
        self.letters = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda',
                        'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']
        self.chars = dict(zip(self.letters, [('Α', 'α'), ('Β', 'β'), ('Γ', 'γ'), ('Δ', 'δ'), ('Ε', 'ε'), ('Ζ', 'ζ'),
                                             ('Η', 'η'), ('Θ', 'θ'), ('Ι', 'ι'), ('Κ', 'κ'), ('Λ', 'λ'), ('Μ', 'μ'),
                                             ('Ν', 'ν'), ('Ξ', 'ξ'), ('Ο', 'ο'), ('Π', 'π'), ('Ρ', 'ρ'), ('Σ', 'σ'),
                                             ('Τ', 'τ'), ('Υ', 'υ'), ('Φ', 'φ'), ('Χ', 'χ'), ('Ψ', 'ψ'), ('Ω', 'ω')]))

        self.get_next()
        self.root.mainloop()

    def check(self, e):
        self.canvas.create_text(*self.coords2, text=self.answer, fill='grey', font=self.font2)
        self.root.update()
        sleep(1)
        self.get_next()

    def get_next(self):
        self.answer = choice(self.letters)

        self.canvas.delete('all')
        self.canvas.create_text(*self.coords, text=self.chars[self.answer][randint(0, 1)], font=self.font)

        self.input.delete(0, END)


if __name__ == '__main__':
    Window()
