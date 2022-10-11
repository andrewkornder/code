#!/usr/bin/python3
# physics2.py

"""Physics simulator for planets in a vacuum"""

from __future__ import annotations

__author__ = "Andrew Kornder"
__version__ = "2.0"

from tkinter import PIESLICE
from math import dist, pi, atan2, asin


# constants
SCALE = 25
GRAVITY = -6.674  # scaled version of newton's constant for gravity, which is 6.674 × 10^11 Newtons per kg^2 m^2
BACKGROUND = '#000000'
OBJ_COLOR = '#808080'
STAT_COLOR = '#FF8800'
LIGHTING_COLOR = '#999999'

# all the planets
planets = []


# this honestly could be done in two lines, the math aint so hard
def gravity(p1: Planet, p2: Planet) -> tuple:
    """
    calculates the force of gravity from p2 to p1
    equation = G * (m1 * m2) / r^2
    
    :param p1: the planet being pulled on
    :param p2: the planet affecting p1
    :return: the force of gravity in an x and y pair
    """

    sx, sy = p1.x - p2.x, p1.y - p2.y

    force = GRAVITY * p1.mass * p2.mass / (sx ** 2 + sy ** 2)  # computing the force of gravity
    force /= p1.mass  # according to F = ma, divide by mass so that the acceleration is lower for heavier objects

    # divide up the force into x and y parts, so the computer can move the oval by that amount
    unit = force / (abs(sx) + abs(sy))
    return unit * sx, unit * sy


def physics() -> None:
    """
    calculates physics and updates Planets accordingly
    
    :return: None
    """

    # TODO: gravity is symmetrical so dont calculate the force of A on B as well as B on A, since they're the same
    for p1 in planets:        
        if p1.sun:  # sun types dont experience pull from other planets, so dont bother calculating them
            continue

        # when there's only one planet, without the starting value of (0, 0), unzipping hates empty lists, so it breaks
        forces = [(0, 0)]
        for p2 in planets:
            if p1 is p2:
                continue

            # on collision, create a new planet from the two old ones, then delete those two, or bounce
            if dist(p1.coords, p2.coords) < p1.radius + p2.radius:
                if p1.colliding or p2.colliding:
                    planets.append(merge(p1, p2))
                    p1.delete()
                    p2.delete()
                else:
                    (p1.dx, p1.dy), (p2.dx, p2.dy) = bounce(p1, p2)

                break
            
            forces.append(gravity(p1, p2))

        # else:  # if the loop finished without a collision
        dx, dy = zip(*forces)  # unzip the list of (dx, dy) tuples into two separate lists of [dx] and [dy]
        p1.dx += sum(dx)  # add up the velocities and add them to the planets velocity
        p1.dy += sum(dy)
        p1.update()


class Planet:
    @classmethod
    def from_preset(cls, canvas, center_x: float | int, center_y: float | int, string: str,
                    colliding: bool, style: str) -> Planet:
        """
        creates a Planet object from a preset

        :param canvas: tkinter.Canvas object that the Planet will be drawn onto
        :param center_x: x coordinate of the center of the screen
        :param center_y: y coordinate of the center of the screen
        :param string: the string encoding the planet's information
        :param colliding: whether the planet should merge or bounce on collision
        :param style: 'circle' or 'rect', the way the planet will be drawn
        :return: a Planet object created from the information
        """

        x, y, name, mass, density, dx, dy, sun = string.split(',')
        # so much type casting
        return cls(canvas, name, (center_x + float(x), center_y + float(y)), (float(dx), float(dy)),
                   float(mass), float(density), bool(int(sun)), colliding, style)

    @staticmethod
    def _get_circle(x: float | int, y: float | int, r: float | int) -> tuple:
        """
        finds the coordinates needed to draw a circle onto a Canvas with position (x, y) and radius r
        
        :param x: x coordinate of center
        :param y: y coordinate of center
        :param r: radius of a circle
        :return: (x, y, x1, y1) set of points
        """

        return x - r, y - r, x + r, y + r

    def __init__(self, canvas, name: str, coords: tuple, velocity: tuple,
                 mass: float | int, density: float | int, sun: bool, colliding: bool, style: str) -> None:
        """
        creates the Planet object
        
        :param canvas: tkinter.Canvas object to be drawn onto
        :param name: name of the planet
        :param coords: (x, y) point of the planet
        :param velocity: (dx, dy) pair of velocities for horizontal and vertical
        :param mass: mass of the planet
        :param density: density of the planet's mass
        :param sun: whether the object is a planet or sun (True => sun, False => planet)
        :param colliding: whether the planet should merge or bounce on collision
        :param style: 'circle' or 'rect', the way the planet will be drawn
        :return: None
        """

        self.x, self.y = coords
        self.dx, self.dy = velocity if not sun else (0, 0)

        self.mass, self.density = mass, density
        volume = mass / density

        # formula for radius of a sphere is cube_root(4/(3pi) * volume), multiplied by a scale for visuals
        self.radius = round((volume / (3 * pi)) ** 0.33 * SCALE, 2)

        self.sun = sun
        self.name = name
        self.colliding = colliding

        self.canvas = canvas
        self.style = style
        self.drawing = None
        self.change_style(style)

        self.lighting = []
        self.create_lighting()

    @property
    def coords(self) -> tuple:
        return self.x, self.y

    def change_type(self):
        """just toggles the collision type"""
        self.colliding = not self.colliding

    def change_style(self, style=None):
        """
        changes the type of drawing made on the canvas
        
        :param style: either 'rect' or 'circle', if left blank, switches from one to the other
        :return: None
        """

        if style not in ('circle', 'rect', None):
            raise ValueError(f'{style} is not a valid drawing method')

        self.canvas.delete(self.drawing)
        if style == 'rect' or (style is None and self.style == 'circle'):
            func = self.canvas.create_rectangle
        elif style == 'circle' or (style is None and self.style == 'rect'):
            func = self.canvas.create_oval
        else:
            print(self.style, style)
            func = self.canvas.create_oval

        self.drawing = func(self._get_circle(*self.coords, self.radius),
                            fill=OBJ_COLOR if not self.sun else STAT_COLOR, outline='')
        self.style = style

    @property
    def velocity(self):  # pretty self-explanatory
        return self.dx, self.dy

    def update(self) -> None:
        """
        updates x, y and the drawing on the screen
        
        :return: None
        """

        self.x += self.dx
        self.y += self.dy

        self.canvas.move(self.drawing, self.dx, self.dy)

        self.canvas.delete(*self.lighting)
        if self.style == 'circle':
            self.create_lighting()

    def delete(self) -> None:
        """
        deletes all relevant parts of object
        
        :return: None
        """

        planets.remove(self)
        self.canvas.delete(self.drawing, *self.lighting)
        del self

    def create_lighting(self):
        """
        draws the light from the suns onto the planet

        :return: None
        """

        if self.sun:
            return

        for obj in planets:
            if not obj.sun:
                continue

            # TODO: find out the size of the arc, maybe the arc-sin of 1/2 * the chord created over the radius (idrk)
            size = 180
            
            sx, sy = self.x - obj.y, self.y - obj.y
            if sx == 0:  # most of the presets would give ZeroDivisionErrors :(
                sx = 0.01

            # finding the angle the light hits at then converting to degrees from radians and adjusting it so it's pointing towards the sun
            angle = atan2(sx, sy) * 180 / pi + 90

            self.lighting.append(self.canvas.create_arc(*self._get_circle(self.x, self.y, self.radius),
                                                        start=angle - size / 2, extent=size, fill=LIGHTING_COLOR,
                                                        style=PIESLICE, outline=''))

    def get_preset_vars(self, center_x, center_y):
        """just retrieves all the data for the planet"""

        return self.x - center_x, self.y - center_y, self.name if self.name else ' ', self.mass, \
            self.density, self.dx, self.dy, int(self.sun)


def bounce(a, b):
    """
    computes the velocities after a 100% elastic collision between two planets, a and b

    :param a: the first planet
    :param b: the second planet
    :return: the velocities for the planets, in the format (A.dx, A.dy, B.dx, B.dy)
    """

    # equation used => http://hyperphysics.phy-astr.gsu.edu/hbase/imgmec/elacol18.gif
    def multiply(x, it): return [x * i for i in it]

    def add(m1, m2): return [x + y for x, y in zip(m1, m2)]

    def sub(m1, m2): return [x - y for x, y in zip(m1, m2)]

    total, diff = (a.mass + b.mass), (a.mass - b.mass)

    # saving values for the equations so i dont have to write them twice
    c, d, e, f = diff / total, 2 / total, a.velocity, b.velocity
    return add(multiply(c, e), multiply(d * b.mass, f)), sub(multiply(d * a.mass, e), multiply(c, f))


def merge(p1: Planet, p2: Planet) -> Planet:
    """
    creates a planet from a collision between two planets

    :param p1: the first planet
    :param p2: the second planet
    :return: the planet created as a result of the collision
    """

    mass = p1.mass + p2.mass
    density = (p1.mass * p1.density + p2.mass * p2.density) / mass  # all guesswork on the equation

    # used the formula for momentum to find dx and dy
    dx = (p1.mass * p1.dx + p2.mass * p2.dx) / mass
    dy = (p1.mass * p1.dy + p2.mass * p2.dy) / mass

    # kind of an arbitrary decision
    name = min(p1, p2, key=lambda a: a.mass).name

    x, y = decide_new_pos(p1, p2)
    canvas = p1.canvas  # they should be the same, if not, then there is a bigger problem
    sun = p1.sun or p2.sun  # suns should always stay suns, planets should stay planets
    style = p1.style  # should be the same
    colliding = p1.colliding or p2.colliding

    return Planet(canvas, name, (x, y), (dx, dy), mass, density, sun, colliding, style)


def decide_new_pos(p1: Planet, p2: Planet) -> tuple:
    """
    calculates a position for the planet that results from a collision

    :param p1: first of two planets
    :param p2: second of two planets
    :return: (x, y) coordinate pair
    """

    # i guessed on how to determine where a new planet would go
    # if we call the larger planet A and the smaller one B and the distance from A to the new planet is D
    # then D over the total distance from A -> B should be the same fraction as the mass of B over the combined mass
    # it turned out pretty well

    # sx and sy are the parts of the slope sy/sx
    # they're used to create a point along the line between the planets
    sx, sy = p1.x - p2.x, p1.y - p2.y

    # dividing the distance into points that'll be split up into the distance D described above
    unit = dist(p1.coords, p2.coords) / (abs(sx) + abs(sy))

    # finding the larger and smaller of the two, since there's no guarantee if p1 or p2 is larger
    b, a = sorted((p1, p2), key=lambda x: x.mass)
    length = unit * b.mass / (a.mass + b.mass)  # (length / unit) should be equal to (D / distance from A -> B)

    dx, dy = length * sx, length * sy  # multiplying by sx and sy to get the right distance
    return a.y + dx, a.y + dy  # getting the point at the right distance from A
