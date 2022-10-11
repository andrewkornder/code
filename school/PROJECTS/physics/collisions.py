from tkinter import Tk, Canvas
from math import pi, dist
from random import randint

FRAME_TIME = 20
SIZE = 800
SCALE = 1000


# TODO: package dxdy_from_vector and window (i wanna use these more often)
def window(size, **kw):
    rt = Tk()
    rt.geometry(f'{size}x{size}')

    cv = Canvas(rt, width=size, height=size)
    for k, v in kw.items():
        if k == 'bg':
            cv['bg'] = v
            rt.configure(bg=v)
        # other shit yk (canvas bg, canvas size, sliders, menus
    cv.pack()

    return rt, cv


def equation(a, b):

    # v1 = (a.m - b.m / t) v1i + 2*b.m / t * v2i
    total = (a.mass + b.mass)
    diff = (a.mass - b.mass)

    c = diff / total
    d = 2 / total
    e, f = a.velocity(), b.velocity()

    v1a = multiply(c, e)
    v1b = multiply(d * b.mass, f)

    v2a = multiply(d * a.mass, e)
    v2b = multiply(c, f)

    v1 = [a + b for a, b in zip(v1a, v1b)]
    v2 = [a - b for a, b in zip(v2a, v2b)]

    return v1, v2


def multiply(x, it):  # just multiplication for a tuple / list (should've used a library for matrix multiplication)
    return [x * a for a in it]


def dxdy_from_vector(force, to, origin):
    """
    takes a line and magnitude and converts it to a change in x and y

    force : a float representing speed
    to : an (x, y) pair of points
    origin : an (x, y) pair of points
    """

    (x, y), (x1, y1) = to, origin
    sx, sy = x - x1, y - y1

    if sx == sy == 0:
        return 0, 0

    unit = force / (abs(sx) + abs(sy))
    dx, dy = unit * sx, unit * sy

    return dx, dy


def random_color():
    r, g, b = [randint(0, 255) for _ in range(3)]
    return f'#{r:02x}{g:02x}{b:02x}'  # rgb to hex


class Object:
    def __init__(self, canvas, x, y, dx=0, dy=0, color=None, mass=3):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.mass = mass
        self.color = color if color is not None else random_color()

        # formula for radius of sphere is the cube root of 3/4 * V/pi
        self.size = ((3 * mass * SCALE) / (4 * pi)) ** (1 / 3)

        self.canvas = canvas
        self.drawing = canvas.create_oval(x - self.size, y - self.size, x + self.size, y + self.size,
                                          fill=self.color)

    def coords(self):
        return self.x, self.y

    def velocity(self):
        return self.dx, self.dy

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.canvas.moveto(self.drawing, self.x, self.y)

        # bounce off the walls
        if not (self.size < self.x < SIZE - self.size):
            self.dx *= -1
        if not (self.size < self.y < SIZE - self.size):
            self.dy *= -1


def collide(p1, p2):
    # basic collision check (only works if the particles aren't traveling too fast

    # TODO: maybe calculate if they collide using actual math? (won't bug out at high speeds)
    if dist(p1.coords(), p2.coords()) < p1.size + p2.size:
        (p1.dx, p1.dy), (p2.dx, p2.dy) = equation(p1, p2)
        return True
    return False


def loop():
    for obj in all_objects:
        for obj2 in all_objects:
            if obj is obj2:
                continue
            if collide(obj, obj2):
                break
        obj.update()

    root.after(FRAME_TIME, loop)


def test():
    testing = 0
    if testing:
        p1 = Object(canv, 50, 400, 2, 0)
        p2 = Object(canv, 400, 400, 3, 0)
        return p1, p2
    else:
        return [Object(canv, randint(50, 750), randint(50, 750),
                       randint(0, 3), randint(0, 3), mass=randint(3, 10))
                for _ in range(20)]


root, canv = window(SIZE, bg='black')
all_objects = test()

if __name__ == '__main__':
    loop()
    root.mainloop()
