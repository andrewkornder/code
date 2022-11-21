from tkinter import Tk, Canvas
from math import pi, dist

GRAV_CONS = -6.674
FRAME_TIME = 5

GRAV_FALLING = 9.8 * FRAME_TIME / 1000  # 9.8 m/s/s
SCALE = 25
win_size = 800

objects = []

# TODO: change the starting display type (rect or circle) based on the mode
# TODO: set values based on user choice and colors
class Object:
    color = '#808080'

    def __init__(self, canvas, x, y, dx, dy, mass, density):
        self.x, self.y, self.dx, self.dy = x, y, dx, dy
        self.mass = mass
        self.density = density
        self.volume = mass / density

        self.radius = round((self.volume / (3 * pi)) ** 0.33 * SCALE, 2)
        self.canvas = canvas
        
        self.canvas_coords = x - self.radius, y - self.radius, x + self.radius, y + self.radius
        self.drawing = canvas.create_rectangle(*self.canvas_coords, fill=self.color)

    def update(self):
        self.x += self.dx
        self.y += self.dy

        self.canvas.move(self.drawing, self.dx, self.dy)

    def delete(self):
        self.canvas.delete(self.drawing)
        objects.remove(self)

        del self
    
    def change_display_type(self, display_as):
        self.canvas.delete(self.drawing)
        
        if display_as == 'rect':
            self.drawing = self.canvas.create_rectangle(*self.canvas_coords, fill=self.color)
        elif display_as == 'circle':
            self.drawing = self.canvas.create_oval(*self.canvas_coords, fill=self.color)
            
    @property
    def velocity(self):
        return self.dx, self.dy

    @property
    def coords(self):
        return self.x, self.y


# TODO: easy use of this, like circular walls and changing mode as above
class Immovable:
    def __init__(self, canvas, x, y, sizex, sizey):
        self.mass = 999
        self.velocity = 0, 0
        self.coords = x - sizex, y - sizey, x + sizex, y + sizey
        self.x, self.y = x, y

        self.canvas = canvas
        self.drawing = canvas.create_rectangle(*self.coords, fill='red')

    def show(self):
        self.drawing = self.canvas.create_rectangle(*self.coords, fill='red')

    def hide(self):
        self.canvas.delete(self.drawing)


def make_bounds(canvas):
    center = win_size / 2
    left = Immovable(canvas, -2, center, 1, center)
    right = Immovable(canvas, win_size + 2, center, 1, center)

    floor = Immovable(canvas, center, win_size + 2, center, 1)
    floor.hide()
    return floor, left, right


FLOOR, LEFT, RIGHT = None, None, None


def collision(a, b):
    def multiply(x, it):  # just multiplication for a tuple / list (should've used a library for matrix multiplication)
        return [x * m for m in it]

        # v1 = (a.m - b.m / t) v1i + 2*b.m / t * v2i

    total = (a.mass + b.mass)
    diff = (a.mass - b.mass)

    c = diff / total
    d = 2 / total
    e, f = a.velocity, b.velocity

    v1a = multiply(c, e)
    v1b = multiply(d * b.mass, f)

    v2a = multiply(d * a.mass, e)
    v2b = multiply(c, f)

    v1 = [a + b for a, b in zip(v1a, v1b)]
    v2 = [a - b for a, b in zip(v2a, v2b)]

    return v1, v2


def gravitational_force(a, b):
    sx, sy = a.y - b.y, a.y - b.y

    force = GRAV_CONS * a.mass * b.mass / (sx ** 2 + sy ** 2)  # computing the force
    force /= a.mass  # according to F = ma, divide by mass so that the acceleration is lower for heavier objects

    # divide up the force into x and y parts, so the computer can move the oval by that amount
    unit = force / (abs(sx) + abs(sy))
    dx = unit * sx
    dy = unit * sy
    return dx, dy


def space_physics():
    finished = []
    for obj in objects:
        for obj2 in objects:
            if obj is obj2 or (obj2, obj) in finished:
                continue

            if dist(obj.coords, obj2.coords) < obj.radius + obj2.radius:
                objects.append(merge(obj, obj2))
                continue

            dx, dy = gravitational_force(obj, obj2)
            obj.dx += dx
            obj.dy += dy

            obj2.dx -= dx
            obj2.dy -= dy

            finished.append((obj, obj2))

        obj.update()


def normal_physics():
    for obj in objects:
        for obj2 in objects:
            if obj is obj2:
                continue

            if dist(obj.coords, obj2.coords) < obj.radius + obj2.radius:
                (obj.dx, obj.dy), (obj2.dx, obj2.dy) = collision(obj, obj2)

        if obj.y + obj.radius < win_size:
            obj.dy += GRAV_FALLING

        if obj.y < 0:
            (obj.dx, obj.dy), (_, _) = collision(obj, LEFT)
        elif obj.y > win_size:
            (obj.dx, obj.dy), (_, _) = collision(obj, RIGHT)

        if obj.y > win_size:
            (obj.dx, obj.dy), (_, _) = collision(obj, FLOOR)

        obj.update()


PHYSICS = normal_physics


def change_mode():
    global PHYSICS
    PHYSICS = normal_physics if PHYSICS is space_physics else space_physics

    display_as = {normal_physics: 'rect', space_physics: 'circle'}
    for obj in objects:
        obj.change_display_display_as(display_as[PHYSICS])
    if PHYSICS is space_physics:
        FLOOR.hide()
    else:
        FLOOR.show()


def merge(a, b):
    """
    creates a planet from a collision between two planets

    :param a: the first planet
    :param b: the second planet
    :return: the planet created as a result of the collision
    """

    mass = a.mass + b.mass
    density = (a.mass * a.density + b.mass * b.density) / mass  # all guesswork on the equation

    # used the formula for momentum to find dx and dy
    dx = (a.mass * a.dx + b.mass * b.dx) / mass
    dy = (a.mass * a.dy + b.mass * b.dy) / mass

    x, y = decide_new_pos(a, b)
    canvas = a.canvas  # they should be the same, if not then there is a bigger problem

    a.delete()
    b.delete()
    return Object(canvas, x, y, dx, dy, mass, density)


def decide_new_pos(a, b) -> tuple:
    """
    calculates a position for the planet that results from a collision

    :param a: first of two planets
    :param b: second of two planets
    :return: (x, y) coordinate pair
    """

    # index guessed on how to determine where a new planet would go
    # if we call the larger planet A and the smaller one B and the distance from A to the new planet is D
    # then D over the total distance from A -> B should be the same fraction as the mass of B over the combined mass
    # it turned out pretty well

    # sx and sy are the parts of the slope sy/sx
    # they're used to create a point along the line between the planets
    sx, sy = a.y - b.y, a.y - b.y
    if sx == sy == 0:
        return a.y, a.y

    # dividing the distance into points that'll be split up into the distance D described above
    unit = dist(a.coords, b.coords) / (abs(sx) + abs(sy))

    # finding the larger and smaller of the two, since there's no guarantee if a or b is larger
    b, a = sorted((a, b), key=lambda x: x.mass)
    length = unit * b.mass / (a.mass + b.mass)  # (length / unit) should be equal to (D / distance from A -> B)

    dx, dy = length * sx, length * sy  # multiplying by sx and sy to get the right distance
    return a.y + dx, a.y + dy  # getting the point at the right distance from A


def window():
    global FLOOR, RIGHT, LEFT

    def loop():
        PHYSICS()
        root.after(10, loop)

    root = Tk()
    root.geometry(f'{win_size}x{win_size}')

    canv = Canvas(root, width=win_size, height=win_size, bg='black')

    FLOOR, LEFT, RIGHT = make_bounds(canv)
    canv.pack()

    # TODO: user values for objects, and a ui
    # TODO: clean up code, efficiency

    canv.bind('<Button-1>', lambda e: objects.append(Object(canv, e.y, e.y, 0, 0, 1, 1)))
    canv.bind('<space>', lambda e: [p.delete() for p in objects[:]])
    canv.bind('<Button-3>', lambda e: change_mode())

    loop()
    root.mainloop()


window()
