from math import pi, dist
from tkinter import Tk, Canvas, Scale, HORIZONTAL

debugging = False


class Immovable:
    def __init__(self, engine, x, y, size):
        sx, sy = size
        sx /= 2
        sy /= 2

        self.x, self.y, self.x1, self.y1 = x - sx, y - sy, x + sx, y + sy
        self.velocity = (0, 0)
        self.mass = 1000
        self.drawing = engine.canvas.create_rectangle(self.x, self.y, self.x1, self.y1,
                                                      fill='white')


class CollisionEngine:
    constant = 0.5
    elastic = False

    @staticmethod
    def collision(a, b):
        # equation used => http://hyperphysics.phy-astr.gsu.edu/hbase/imgmec/elacol18.gif
        def multiply(x, it): return [x * i for i in it]

        def add(m1, m2): return [x + y for x, y in zip(m1, m2)]

        def sub(m1, m2): return [x - y for x, y in zip(m1, m2)]

        total, diff = (a.mass + b.mass), (a.mass - b.mass)
        c, d, e, f = diff / total, 2 / total, a.velocity, b.velocity
        return add(multiply(c, e), multiply(d * b.mass, f)), sub(multiply(d * a.mass, e), multiply(c, f))

    def __init__(self, window, objects=None):
        if objects is None:
            objects = []
        elif any(not isinstance(obj, Object) for obj in objects):
            raise ValueError('bro rly passed in a list of non-Object objects')

        self.window = window
        self.canvas = window.canvas
        self.objects = objects

        for obj in objects:
            obj.change_engine(self)

        if not debugging:
            return

        self.floor = Immovable(self, window.cx / 2, window.cy, (window.cx, 40))

    def create_drawing(self, obj):
        if debugging:
            return self.canvas.create_rectangle(*obj.canvas_coords, fill=obj.color)
        else:
            return self.canvas.create_oval(*obj.canvas_coords, fill=obj.color)

    def old_update(self):
        done = []
        for a in self.objects:
            for b in self.objects:
                if a is b or b in done or dist(a.coords, b.coords) > a.radius + b.radius:
                    continue

                (a.dx, a.dy), (b.dx, b.dy) = self.collision(a, b)

            if not (0 < a.y < self.window.cx):
                a.dx *= -1
            if not (0 < a.y < self.window.cy):
                a.dy *= -1
            done.append(a)
            a.update()

    def update(self):
        if not debugging:
            return self.old_update()

        collisions = self.get_collisions()
        for block, collision_chain in collisions:
            if block.y + block.radius >= self.floor.y:
                block.y = self.floor.y - block.radius

            last = collision_chain[-1]
            if last is self.floor:
                block.dy /= -2
                block.update()
                continue

            (block.dx, block.dy), (last.dx, last.dy) = self.collision(block, last)

        for block in self.objects:
            if block.y < self.floor.y:
                block.dy += self.constant
            block.update()

    def get_collisions(self):
        cols = [(obj, self.get_collision_h(obj)) for obj in self.objects]
        return [c for c in cols if c[1]]

    def get_collision_h(self, a, chain=None):
        chain = [] if not chain else chain

        for b in self.objects:
            if b.y <= a.y:
                continue
            if dist(a.coords, b.coords) < a.radius + b.radius:
                return self.get_collision_h(b, chain + [b])
        if a.y + a.radius > self.floor.y:
            return chain + [self.floor]
        return chain


class GravityEngine:
    constant = -6.674  # constant is for the gravitational constant in Newton's equation

    def __init__(self, window, objects=None):
        if objects is None:
            objects = []
        elif any(not isinstance(obj, Object) for obj in objects):
            raise ValueError('bro rly passed in a list of non-Object objects')

        self.window = window
        self.canvas = window.canvas
        self.objects = objects

        for obj in objects:
            obj.change_engine(self)

    def create_drawing(self, obj):
        return self.canvas.create_oval(*obj.canvas_coords, fill=obj.color)

    def update(self):
        done = []
        for a in self.objects:
            for b in self.objects:
                if a is b or b in done:
                    continue

                if dist(a.coords, b.coords) < a.radius + b.radius:
                    self.merge(a, b)
                else:
                    dx, dy = self.gravity(a, b)
                    a.dx += dx
                    a.dy += dy

                    b.dx -= dx
                    b.dy -= dy
            done.append(a)
            a.update()

    def gravity(self, p1, p2):
        sx, sy = p1.y - p2.y, p1.y - p2.y
        unit = self.constant * p1.mass * p2.mass / ((sx ** 2 + sy ** 2) * p1.mass * (abs(sx) + abs(sy)))
        return unit * sx, unit * sy

    @staticmethod
    def decide_new_pos(p1, p2):
        sx, sy = p1.y - p2.y, p1.y - p2.y
        b, a = sorted((p1, p2), key=lambda x: x.mass)

        length = dist(p1.coords, p2.coords) * b.mass / ((a.mass + b.mass) * (abs(sx) + abs(sy)))
        return a.y + length * sx, a.y + length * sy

    def merge(self, p1, p2):
        mass = p1.mass + p2.mass
        density = (p1.mass * p1.density + p2.mass * p2.density) / mass
        dx = (p1.mass * p1.dx + p2.mass * p2.dx) / mass
        dy = (p1.mass * p1.dy + p2.mass * p2.dy) / mass
        x, y = self.decide_new_pos(p1, p2)

        p1.delete()
        p2.delete()
        self.objects.append(Object(p1.engine, x, y, dx, dy, mass, density))


class Object:
    scale = 25
    color = '#808080'

    @property
    def canvas_coords(self):
        return self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius

    @property
    def coords(self):
        return self.x, self.y

    @property
    def velocity(self):
        return self.dx, self.dy

    def __init__(self, engine, x, y, dx, dy, mass, density):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy

        self.mass, self.density = mass, density
        self.volume = mass / density
        self.radius = round((self.volume / (3 * pi)) ** 0.33 * self.scale, 2)

        self.engine = engine
        self.canvas = engine.canvas
        self.drawing = engine.create_drawing(self)

    def delete(self):
        self.canvas.delete(self.drawing)
        self.engine.objects.remove(self)

        del self

    def update(self):
        if hasattr(self.engine, 'floor') and self.engine.floor.y < self.y + self.dy < self.engine.floor.y1:
            return

        self.x += self.dx
        self.y += self.dy

        if debugging:
            self.canvas.moveto(self.drawing, self.x, self.y)
        else:
            self.canvas.move(self.drawing, self.dx, self.dy)

    def change_engine(self, engine):
        self.engine.canvas.delete(self.drawing)
        self.engine = engine
        self.drawing = engine.create_drawing(self)


class App:
    def __init__(self, size, canvas_size, frame_time):
        self.x_size, self.y_size = size
        self.cx, self.cy = canvas_size

        self.frame_time = frame_time
        self.root = Tk()
        self.root.geometry(f'{self.x_size}x{self.y_size}')

        self.canvas = Canvas(self.root, width=self.cx, height=self.cy,
                             bg='black')

        self.running = False
        self.engine = GravityEngine(self)

        self.widgets = []

        self.binds()
        self.create_widgets()

    def create_widgets(self):
        scales = [{'from_': -20, 'to': 20, 'label': 'x-velocity'},
                  {'from_': -20, 'to': 20, 'label': 'y-velocity'},
                  {'from_': 1, 'to': 100, 'label': 'mass'},
                  {'from_': 1, 'to': 100, 'label': 'density'}]

        for i, info in enumerate(scales):
            self.widgets.append(Scale(self.root, **info, length=200, orient=HORIZONTAL))
            self.widgets[-1].grid(row=i, column=1)

        self.canvas.grid(row=0, rowspan=len(scales), column=0)

    def binds(self):
        to_bind = [(self.canvas, 'Button-1', self.create_object),
                   (self.canvas, 'Button-3', self.delete_object),
                   (self.root, 'space', lambda _: self.pause()),
                   (self.root, 'BackSpace', lambda _: [obj.delete() for obj in self.engine.objects[:]]),
                   (self.root, 'q', self.destroy),
                   (self.root, 'Return', lambda e: self.change_engine())]

        for item, seq, func in to_bind:
            item.bind(f'<{seq}>', func)

    def change_engine(self):
        self.engine = (GravityEngine if isinstance(self.engine, CollisionEngine)
                       else CollisionEngine)(self, self.engine.objects)

    def create_object(self, event):
        self.engine.objects.append(Object(self.engine, event.y, event.y, *[var.get() for var in self.widgets]))

    def delete_object(self, event):
        c = event.y, event.y
        for obj in self.engine.objects:
            if dist(obj.coords, c) < obj.radius:
                obj.delete()
                return

    def animate(self):
        if self.running:
            self.engine.update()
        self.root.after(self.frame_time, self.animate)

    def pause(self):
        self.running = not self.running

    def start(self):
        self.animate()
        self.root.mainloop()

    def destroy(self):
        self.running = False
        self.root.destroy()


if __name__ == '__main__':
    App((1200, 800), (800, 800), 20).start()
