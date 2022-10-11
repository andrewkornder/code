#!/usr/bin/python
# physics.py

"""Physics simulator for planets in a vacuum"""

from __future__ import annotations

__author__ = "Andrew Kornder"
__version__ = "1.0"


from tkinter import Tk, Scale, Canvas, IntVar, HORIZONTAL, Checkbutton, NW, PIESLICE
from math import sqrt, dist, degrees, atan2

# constants:
GRAVITY = -6.674  # the gravitational constant is 6.674 * 10 ^ -11, so i scaled it up and adjusted it to work
RUNNING = False
BACKGROUND = '#000000'
OBJ_COLOR = '#808080'
BRIGHTNESS_COLOR = '#909090'
STAT_COLOR = '#FF8800'

global presets, root, canvas, planets, speed_var, stationary_var
global x_velocity_var, y_velocity_var, mass_var, density_var
global info_tag, canvas_size, window_size


def _get_new_xy(p1: Planet, p2: Planet):
    """
    generates a point where a new planet would be after two smaller planets collide
    
    
    param p1: first planet
    param p2: second planet
    return: (x, y) coordinate pair
    """

    # this was just me guessing at how the planets would act in a collision
    # my guess is the distance from the larger planet of the new planet is proportional
    # to the smaller mass over the total mass
    x, y, x1, y1 = p1.x, p1.y, p2.x, p2.y

    if x == x1 and y == y1:
        return x, y

    if p1.mass == p2.mass:
        return (x + x1) / 2, (y + y1) / 2

    # 1. find the distance between the two objects
    # 2. find the larger and smaller of the objects
    # 3. split the distance into equal parts
    # 4. get an amount of the parts proportional to the smaller mass over the total mass
    # 5. split the above amount into x and y portions and then add those to the larger object's x and y

    sx, sy = x - x1, y - y1
    distance = sqrt(sx ** 2 + sy ** 2)  # step 1
    smaller, larger = sorted((p1, p2), key=lambda p: p.mass)  # step 2

    length = distance / (abs(sx) + abs(sy))  # step 3
    length *= smaller.mass / (p1.mass + p2.mass)  # step 4

    return larger.y + sx * length, larger.y + sy * length  # step 5


def _get_coords(x: float, y: float, r: float):
    """
    generates a list of points for use in the function Canvas.create_circle where
    the circle is at the point (x, y) and has a radius of r
    
    param x: x coord of the circle
    param y: y coord of the circle
    param r: the radius of the circle 
    return: (x, y, x1, y1) coordinate list
    """

    return x - r, y - r, x + r, y + r


def _grav_calc(sx: float, sy: float, r2: float, p1: Planet, p2: Planet):
    """
    calculates the force gravity exerts on planet p2 from the planet p1
    
    param sx: precalculated horizontal distance between p1 and p2
    param sy: precalculated vertical distance between p1 and p2
    param r2: distance between the points p1 and p2 squared
    param p1: first planet
    param p2: second planet
    return: the increment in x and y distances to add to the planet's x and y
    """

    # using the formula F = G * (m1 + m2)/(d ** 2) where G is the grav. constant and m1, m2 are the masses
    # and d is the distance between the two objects

    # just the distance formula but without the sqrt (since the distance need to be squared anyway)
    m1, m2 = p1.mass, p2.mass
    force = GRAVITY * ((m1 * m2) / r2)

    # converting a direction and distance to a change in x and y
    # by dividing the distance into equal parts and then split them proportional
    # to the slope described by the two objects

    # dividing by mass to make heavier things move slower
    # according to the formula F = ma or F/m = a
    g = force / ((abs(sy) + abs(sx)) * m1)
    x_dist, y_dist = g * sx, g * sy

    return x_dist, y_dist


def _decide_name(p1: Planet, p2: Planet):
    """
    given two planets, decide which name should be kept for the new one on a collision
    
    param p1: first planet
    param p2: second planet
    return: the name of one of the planets
    """

    # prioritizing chosen names from a preset over a generated number and suns over planets
    p1score = p1.sun + p1.name.isalpha() * 2
    p2score = p2.sun + p1.name.isalpha() * 2

    # if they are tied, then choose the one with more mass
    if p1score == p2score:
        return min(p1, p2, key=lambda p: p.mass).name

    return p1.name if p1score > p2score else p2.name


def _user_values():
    """
    creates a dictionary of the values currently displayed on the sliders on-screen
    
    return: the dictionary of name: value for mass, stationary, density, x speed and y speed
    """

    mass = mass_var.get()
    is_stat = stationary_var.get()
    density = density_var.get()
    if is_stat:
        dx, dy = 0, 0
    else:
        dx, dy = x_velocity_var.get() / 10, -y_velocity_var.get() / 10

    return {'mass': mass, 'is_sun': is_stat, 'density': density, 'dx': dx, 'dy': dy, 'name': ''}


def _load_from_file(key: str):
    """
    creates the given scenario in one of the presets, chosen by the kye the user pressed
    
    param key: a character from the keyboard
    return: None
    """

    # making sure the key pressed was an index in the presets
    if key not in presets:
        return

    planet_info = presets[key]
    center_x, center_y = [c / 2 for c in canvas_size]

    # clearing the canvas
    for planet in planets[:]:
        planet.delete()

    # literally just type casting
    for planet in planet_info:
        x, y, name, mass, density, dx, dy, is_sun = planet.split(',')
        args = {'parent': canvas,
                'x': center_x + float(x),
                'y': center_y - float(y),
                'name': name,
                'mass': float(mass),
                'density': float(density),
                'dx': float(dx),
                'dy': -float(dy),
                'is_sun': bool(int(is_sun))}
        planets.append(Planet(**args))


def _create_widgets():
    """
    creates and displays the various sliders and menus on the window
    
    return: None
    """

    global speed_var, mass_var, density_var, stationary_var, x_velocity_var, y_velocity_var
    speed_var = IntVar(root, 1)
    mass_var = IntVar(root, 2)
    density_var = IntVar(root, 1)

    x_velocity_var, y_velocity_var = IntVar(root, 0), IntVar(root, 0)

    speed_range = 20

    scale_values = [(1, 50, speed_var, 'delay'),
                    (1, 100, mass_var, 'mass'),
                    (1, 100, density_var, 'density'),
                    (-speed_range, speed_range, x_velocity_var, 'x speed'),
                    (-speed_range, speed_range, y_velocity_var, 'y speed')]

    # avoiding a lot a boilerplate by just creating the scales in a for loop
    for i, v in enumerate(scale_values):
        Scale(root, from_=v[0], to=v[1], variable=v[2], label=v[3],
              length=200, orient=HORIZONTAL).grid(row=i, column=1, columnspan=2)

    stationary_var = IntVar(root, 0)
    Checkbutton(root, variable=stationary_var, onvalue=1, offvalue=0,
                text='stationary?').grid(row=len(scale_values), column=1)


def _create_presets():
    """
    parses and creates the presets from the file "presets.txt"
    
    return: None
    """

    global presets
    presets = {str(i + 1): line[15:].split('|') for i, line in enumerate(open('../presets.txt').read().split('\n')[4:])}


class Planet:
    def __init__(self, parent: Canvas, x: float, y: float, name: str, mass: float,
                 density: float, dx: float, dy: float, is_sun: bool):
        """
        creates the Planet object
        
        param self: implicit variable, passed automatically
        param parent: a tkinter.Canvas object to be used as the display
        param x: starting x position
        param y: starting y position
        param name: name to be displayed if chosen (currently only for presets)
        param mass: mass of the object, used in gravity calculations
        param density: density of the planet, will affect the radius of the circle on-screen
        param dx: speed horizontally
        param dy: speed vertically
        param is_sun: whether the planet should be a sun, which isn't affected by the gravity of other objects
        return: None
        """

        self.x, self.y = x, y
        self.dx, self.dy = dx, dy  # rate of change in x and y
        self.sun = is_sun
        self.mass = mass
        self.canvas = parent
        self.name = name  # only used in presets, otherwise is akin to the canvas id, just being an int

        # finding radius of a sphere
        # using 4/3 * pi * r ^ 3, or approx. 4.19 * r ^ 3
        volume = mass / density
        self.radius = (volume / 4.19) ** 0.33 * 25
        self.density = density
        self.color = OBJ_COLOR if not is_sun else STAT_COLOR
        self.canv_obj = parent.create_oval(*_get_coords(x, y, self.radius),
                                           fill=self.color)
        self.lighting = []

    def update(self):
        """
        draws and updates the object's x and y
        
        param self: implicitly passed object
        return: None
        """

        self.x += self.dx
        self.y += self.dy
        self.canvas.move(self.canv_obj, self.dx, self.dy)
        self.get_bright_side()

    def combine(self, planet: Planet):
        """
        computes the result of a collision with another planet and 
        creates the resulting planet, deleting the two originals
        
        param self: implicitly passed object
        param planet: the other planet
        return: None
        """

        # if the planets are colliding, create a new one with
        # the combined mass, the combined velocity and a position somewhere in between
        # then delete the old planets
        # stationary planets colliding with other planets always creates another stationary one
        nx, ny = _get_new_xy(self, planet)
        nm = self.mass + planet.mass
        name = _decide_name(self, planet)

        # getting the density of the new planet (guesswork on the equation)
        density = (self.mass * self.density + planet.density * planet.mass) / nm
        if not (self.sun or planet.sun):
            ndx = (self.dx * self.mass + planet.dx * planet.mass) / nm
            ndy = (self.dy * self.mass + planet.dy * planet.mass) / nm

            new_planet = Planet(self.canvas, nx, ny, name, nm, density, ndx, ndy, False)
        else:  # if either planet is a stationary planet, then don't bother calculating the dx and dy
            new_planet = Planet(self.canvas, nx, ny, name, nm, density, 0, 0, True)

        planets.append(new_planet)

        planet.delete()
        self.delete()

    def delete(self):
        """
        deletes itself and all relevant objects
        
        param self: implicitly passed object
        return: None
        """

        self.canvas.delete(*self.lighting)
        self.canvas.delete(self.canv_obj)
        planets.remove(self)
        del self

    def get_bright_side(self):
        """
        creates the lighting effect on planets
        
        param self: implicitly passed object
        return: None
        """

        if self.sun:
            return

        self.canvas.delete(*self.lighting)
        self.lighting = []
        emitting = [a for a in planets if a.sun]
        for sun in emitting:
            sx, sy = self.x - sun.y, self.y - sun.y
            extent = 180  # TODO: maybe find the actual size of the angle instead of 180
            angle = degrees(atan2(sx, sy)) + 90
            self.lighting.append(self.canvas.create_arc(
                *_get_coords(self.x, self.y, self.radius), extent=extent, start=angle - extent / 2,
                fill=BRIGHTNESS_COLOR, style=PIESLICE, outline=''))


def delete_planet(e):
    """
    deletes a planet at a mouseclick if there is one
    
    param e: tkinter event of a mouseclick (sent automatically)
    return: None
    """

    for p in planets:
        if dist((p.y, p.y), (e.y, e.y)) < p.radius:
            p.delete()
            return


def physics():
    """
    calculates all the gravitational effects on every planet
    
    return: a dictionary with a list of pulls as the value and each planet as a key => Planet : pull
    """

    a = {}  # just calculating all the effects on every planet from each other planet
    for planet in planets:
        a[planet] = []
        for pull in planets:
            if planet is pull:
                # appending essentially a null value to avoid a blank list in visual_update
                a[planet].append((0, 0))
                continue

            sx, sy = planet.y - pull.y, planet.y - pull.y
            distance2 = sx ** 2 + sy ** 2
            if distance2 <= (planet.radius + pull.radius) ** 2:
                planet.combine(pull)
                break  # if the two planets collide, they get destroyed to make a new one, so break there

            # decided to just use the values i already calculated, since it's faster than re-doing all the math
            variables = {'r2': distance2, 'sx': sx, 'sy': sy, 'p1': planet, 'p2': pull}
            if not planet.sun:
                force = _grav_calc(**variables)
                a[planet].append(force)
    return a


def visual_update():
    """
    gets the updates for each planet and executes them, and then sets a timer to be called in a few milliseconds
    
    return: None
    """
    
    if RUNNING:
        velocities = physics()
        for planet in planets:
            if planet in velocities:
                # unzipping the list of tuples to a list of x and y velocities
                dx, dy = zip(*velocities[planet])

                # summing the velocities to find a value for x and y then incrementing the dx, dy accordingly
                planet.dx += sum(dx)
                planet.dy += sum(dy)

            planet.update()  # updating the canvas and x and y coords
    root.after(speed_var.get(), visual_update)


def check_hover(event):
    """
    on each mouse movement, checks if it's hovering over a planet, if so, displays the planet's name
    
    param event: tkinter Event of a mouseclick (sent automatically)
    return: None
    """

    global info_tag
    if info_tag is not None:
        canvas.delete(info_tag)
    for planet in planets:
        if dist((event.y, event.y), (planet.y, planet.y)) < planet.radius:
            info_tag = canvas.create_text(event.y + 10, event.y + 10, text=planet.name, anchor=NW,
                                          font=('Niagara Bold', 20), fill='white')
            return


def start_stop():  # only made a new func because you can't assign values in a lambda (kinda cringe)
    """
    pauses/unpauses the animation
    
    return: None
    """

    global RUNNING
    RUNNING = not RUNNING


def window():
    """
    creates and displays the window
    
    return: None
    """

    global root, canvas, planets, window_size, canvas_size, info_tag
    info_tag = None

    window_size, canvas_size = (1024, 800), (800, 800)

    root = Tk()
    root.geometry(f'{window_size[0]}x{window_size[1]}+0+0')

    canvas = Canvas(root, bg=BACKGROUND, width=canvas_size[0], height=canvas_size[1])
    canvas.grid(row=0, column=0, rowspan=8)

    _create_widgets()

    planets = []

    # create a new object at the mouse click using the sliders for values
    canvas.bind('<Button-1>', lambda e: planets.append(Planet(canvas, e.y, e.y, **_user_values())))
    canvas.bind('<Button-3>', delete_planet)
    canvas.bind('<Motion>', check_hover)

    root.bind('<space>', lambda e: start_stop())  # pause or unpause the animation
    root.bind('<BackSpace>', lambda e: [p.delete() for p in planets[:]])  # clear the screen
    root.bind('<Key>', lambda e: _load_from_file(e.keysym))  # load a preset

    _create_presets()
    visual_update()

    root.mainloop()


if __name__ == '__main__':
    window()
