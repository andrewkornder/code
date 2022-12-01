from math import dist
from tkinter import Tk, Canvas


def lerp_1d(a, b, t):
    return a + t * (b - a)


def lerp(ax, ay, bx, by, t):
    return lerp_1d(ax, bx, t), lerp_1d(ay, by, t)


class Point:
    def __init__(self, x, y, radius, canvas, color, child=False, draw=True):
        self.x, self.y = x, y
        if draw:
            self.drawing = canvas.create_oval(x - radius, y - radius,
                                              x + radius, y + radius,
                                              fill=color, outline='' if not child else 'white',
                                              tags=('point',) + () if not child else ('child',))
        self.canvas = canvas
        self.color = color
        self.radius = radius

    def lerp(self, b, t, illus=True):
        if illus:
            self.canvas.create_line(*self.coords, *b.coords, fill='white', width=self.radius / 5, tags=('child',))
        return Point(*lerp(*self.coords, *b.coords, t), self.radius / 2, self.canvas, 'orange', child=True, draw=illus)

    @property
    def coords(self):
        return self.x, self.y

    def move_delta(self, dx, dy, trail=False):
        if trail:
            self.canvas.create_line(*self.coords, self.x + dx, self.y + dy, fill=self.color, tags=('trails',))
        self.canvas.move(self.drawing, dx, dy)
        self.x, self.y = self.x + dx, self.y + dy

    def move(self, x, y, trail=False):
        if trail:
            self.canvas.create_line(*self.coords, x, y, fill=self.color, tags=('trails',))
        self.x, self.y = x, y
        self.canvas.moveto(self.drawing, x - self.radius, y - self.radius)

    def __repr__(self):
        return f'Point({self.x}, {self.y})'


def bezier(vectors, t, illus):
    if len(vectors) == 2:
        a, b = vectors
        if illus:
            a.canvas.create_line(*a.coords, *b.coords, fill='white', tags=('child',), width=a.radius / 5)
        return lerp(*a.coords, *b.coords, t)
    return bezier([vectors[i].lerp(p, t, illus) for i, p in enumerate(vectors[1:])], t, illus)


class Rotator:
    def __init__(self, *iterable):
        self.iterable, self.i = iterable if len(iterable) > 1 else iterable[0], 0

    @property
    def next(self):
        self.i += 1
        return self.iterable[(self.i - 1) % len(self.iterable)]


class Graph:
    ms, increment = 10, 0.005

    def __init__(self, w, h):
        self.root = Tk()
        self.root.geometry(f'{w}x{h}')

        self.canvas = Canvas(self.root, width=w, height=h, bg='black')
        self.canvas.pack()

        self.canvas.bind('<Button-1>', lambda e: self.add_point(e.x, e.y))
        self.root.bind('<BackSpace>', lambda e: self.reset())
        self.root.bind('<space>', lambda e: self.pause())
        self.root.bind('<s>', lambda e: self.toggle_lines())

        self.canvas.bind('<ButtonPress-3>', lambda e: self.toggle_pressed())
        self.canvas.bind('<Motion>', lambda e: self.drag(e.x, e.y))
        self.canvas.bind('<ButtonRelease-3>', lambda e: self.toggle_pressed())

        self.points = []
        self.bezier = None
        self.paused = False
        self.rpressed = False
        self.lines = True
        self.t = 0

        self.radius = 3
        self.play()

    def toggle_lines(self):
        self.lines = not self.lines

    def add_point(self, x, y):
        self.points.append(Point(x, y, self.radius, self.canvas, 'red'))
        if self.bezier is None and len(self.points) >= 2:
            self.bezier = Point(*self.points[0].coords, self.radius, self.canvas, 'white')
        if self.bezier:
            self.restart()

    def pause(self):
        self.paused = not self.paused

    def play(self):
        if self.paused or len(self.points) < 2:
            self.root.after(self.ms, self.play)
            return

        if self.t >= 1:
            self.restart()
        self.canvas.delete('child')
        self.bezier.move(*bezier(self.points, self.t, self.lines), trail=True)
        self.t += self.increment
        self.root.after(self.ms, self.play)

    def reset(self):
        self.points = []
        self.canvas.delete('all')
        self.t = 0
        self.bezier = None

    def restart(self):
        self.bezier.move(*self.points[0].coords)
        self.canvas.delete('trails')
        self.t = 0

    def toggle_pressed(self):
        self.rpressed = not self.rpressed

    def drag(self, x, y):
        if not self.rpressed:
            return

        for point in self.points:
            if dist(point.coords, (x, y)) < self.radius:
                point.move(x, y)
                return

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    _g = Graph(1000, 1000)

    k = 10
    n = 1
    for i in range(k):
        for c in ((0, 0), (1000, 0), (1000, 1000), (0, 1000))[:4 if k - i - 1 else n]:
            _g.add_point(*c)

    _g.run()
