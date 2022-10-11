#!/usr/bin/python
# runner.py

"""App for running a physics simulation"""

from __future__ import annotations

__author__ = "Andrew Kornder"
__version__ = "2.0"


from math import dist
from tkinter import Tk, Scale, Canvas, IntVar, StringVar, HORIZONTAL, Checkbutton, Entry, OptionMenu, Button, Event, \
    Toplevel
from physics2 import physics, planets, Planet


class App:
    def __init__(self) -> None:
        """
        creates the App object

        :return: None
        """

        self.running = False
        self.width, self.height = 1400, 900
        self.canvas_width, self.canvas_height = 900, 900
        self.center = 450, 450
        
        self.root = Tk()
        self.root.title('Planets')
        self.root.geometry(f'{self.width}x{self.height}+100+20')
        
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.name_display = None

        # lots of tkinter Vars for the user to pick values for the planets
        self.speed_var = IntVar(self.root, 5)
        self.mass_var, self.density_var = IntVar(self.root, 2), IntVar(self.root, 1)
        self.x_vel_var, self.y_vel_var = IntVar(self.root, 0), IntVar(self.root, 0)
        self.sun_var = IntVar(self.root, 0)
        self.name_var = StringVar(self.root, '')
        self.om = None

        self.file = '../presets.txt'
        self.presets = self.create_presets(self.file)
        self.current_preset = StringVar(self.root, 'select preset')  # dropdown menu

        self.widgets()
        self.binds()
        
        self.style, self.colliding = 'circle', True

    def start_stop(self) -> None:
        """
        pauses or unpauses the animation

        :return: None
        """

        self.running = not self.running

    def widgets(self) -> None:
        """
        creates various sliders, buttons and menus on the window

        :return: None
        """
        
        # avoiding a little copy-pasting by making scales in a for loop
        scales = [{'from_': 1, 'to': 50, 'variable': self.speed_var, 'label': 'delay'},
                  {'from_': -20, 'to': 20, 'variable': self.x_vel_var, 'label': 'x-velocity'},
                  {'from_': -20, 'to': 20, 'variable': self.y_vel_var, 'label': 'y-velocity'},
                  {'from_': 1, 'to': 100, 'variable': self.mass_var, 'label': 'mass'},
                  {'from_': 1, 'to': 100, 'variable': self.density_var, 'label': 'density'}]

        for i, info in enumerate(scales):
            Scale(self.root, **info, length=200, orient=HORIZONTAL).grid(row=i, column=2, columnspan=2)

        # adding the canvas in here, so it's relative to the scales, since they have to be the same height
        self.canvas.grid(row=0, rowspan=len(scales) + 2, column=1)  
        
        Checkbutton(self.root, variable=self.sun_var, onvalue=1, offvalue=0,
                    text='sun').grid(row=len(scales), column=2)
        
        Entry(self.root, textvariable=self.name_var, width=10).grid(row=len(scales) + 1, column=2)  # user-inputted name

        self.om = OptionMenu(self.root, self.current_preset, *self.presets)
        self.om.grid(row=0, column=0, padx=50)  # dropdown menu

        Button(self.root, command=self.load_preset, text='load preset').grid(row=1, column=0)  # load button
        
        Button(self.root, command=self.change_collision, text='change collision type').grid(row=2, column=0)
        Button(self.root, command=self.change_drawing, text='change drawing type').grid(row=3, column=0)

    def save_preset(self):
        """
        saves the current position and velocities of all the planets into a preset that can be accessed later using
        the dropdown menu

        :return: None
        """

        def check_limit():
            # there's gotta be a better way to do this, but it just caps the entry length at 11
            if len(name.get()) > 11:
                name.set(name.get()[:11])

        def write_preset():
            """takes the information and writes to the current file, then updates the app and closes the popup"""

            # writing to the file
            title = name.get() + ' ' * (11 - len(name.get()))
            open(self.file, 'a').write(f'\n{title} => {get_preset_vars()}')

            # updating the dropdown and presets
            self.om['menu'].add_command(label=name.get(), command=lambda n=name.get(): self.current_preset.set(n))
            self.presets = self.create_presets(self.file)
            top.destroy()

        def get_preset_vars():
            """retrieves and formats the information for every planet"""

            return '|'.join(','.join(map(str, planet.get_preset_vars(*self.center))) for planet in planets)

        # creates the popup and customizes it
        top = Toplevel(self.root)
        top.title('Save preset?')
        top.geometry('300x100')

        # variable for the entry, bound to the function that caps the text at 11 chars
        name = StringVar(top)
        name.trace_add("write", lambda *_: check_limit())

        entry = Entry(top, width=11, textvariable=name)
        entry.pack()

        # button to enter the name, will also close the popup and write the data to the file
        Button(top, text='Save current system as preset?', command=write_preset).pack()

    def change_collision(self):
        """
        switches the style of collision for all planets in the simulation
        
        :return: None
        """
        
        for obj in planets:
            obj.change_type()
        self.colliding = not self.colliding
    
    def change_drawing(self):
        """
        switches the style of drawing for all planets in the app
        
        :return: None
        """
        
        self.style = 'circle' if self.style == 'rect' else 'rect'
        for obj in planets:
            obj.change_style(self.style)
            
    def binds(self) -> None:
        """
        binds a list of events to functions at start-up

        :return: None
        """
        
        # it's just easier to look at and add stuff this way
        to_bind = [(self.canvas, 'Motion', self.hover),
                   (self.canvas, 'Button-1', self.create_planet),
                   (self.canvas, 'Button-3', self.delete_at_click),
                   (self.root, 'space', lambda _: self.start_stop()),
                   (self.root, 'BackSpace', lambda _: [planet.delete() for planet in planets[:]]),
                   (self.root, 'q', lambda _: self.destroy()),
                   (self.root, 'Control-s', lambda _: self.save_preset())]
        
        for item, seq, func in to_bind:
            item.bind(f'<{seq}>', func)
        
    def create_planet(self, event: Event) -> None:
        """
        creates a planet with user information at the current mouse location

        :param event: tkinter.Event object with information about a mouse-click
        :return: None
        """

        x, y = event.x, event.y
        dx, dy = self.x_vel_var.get(), self.y_vel_var.get()

        mass, density = self.mass_var.get(), self.density_var.get()
        sun = self.sun_var.get()

        name = self.name_var.get()
        self.name_var.set('')  # erasing the name in the Entry
        
        planets.append(Planet(self.canvas, name, (x, y), (dx, dy),
                              mass, density, bool(sun), self.colliding, self.style))

    def frame(self) -> None:
        """
        updates the window with a new frame

        :return: None
        """

        # pretty self-explanatory tbh
        if self.running:
            physics()

        self.root.after(self.speed_var.get(), self.frame)
    
    def load_preset(self) -> None:
        """
        loads a preset when called, deleting any other planets

        :return: None
        """

        key = self.current_preset.get()
        if key == 'select preset':
            return  # default value isn't a key in the dictionary

        for planet in planets[:]:  # clear the screen
            planet.delete()

        preset = self.presets[key]
        for planet in preset:
            # adding the planets into the scene
            planets.append(Planet.from_preset(self.canvas, *self.center, planet, self.colliding, self.style))
    
    @staticmethod
    def delete_at_click(event: Event) -> None:
        """
        deletes a planet if the mouse right-clicked on one

        :param event: tkinter.Event object holding information about the mouse-click
        :return: None
        """

        coords = event.x, event.y
        for planet in planets:
            if dist(coords, planet.coords()) < planet.radius:
                planet.delete()
                return  # not deleting more than 1

    @staticmethod
    def create_presets(file: str) -> dict:
        """
        creates a dictionary of the presets in the form [preset name]: [preset information]

        :param file: the file with the presets in it
        :return: a dictionary with the titles mapped to the information for the preset
        """

        # dictionary comprehensions :)
        # just saying skip the first four lines and then take all the characters from 12 and on as the info
        # for more information, read the header in presets.txt
        return {line[:12].strip(): line[15:].split('|') for i, line in enumerate(open(file).read().split('\n')[4:])}
    
    def hover(self, event: Event) -> None:
        """
        displays a popup name-tag if the mouse is above a planet

        :param event: tkinter.Event object with information about the mouse's position
        :return: None
        """

        if self.name_display is not None:  # only is None on the first run
            self.canvas.delete(self.name_display)

        coords = event.x, event.y
        for planet in planets:
            if dist(coords, planet.coords) < planet.radius:
                self.name_display = self.canvas.create_text(event.x + 20, event.y + 20, text=planet.name,
                                                            fill='white', font=('Niagara Bold', 10))
                return  # offset of 20 because otherwise the cursor blocks the text, so gotta make it visible

    def start(self) -> None:
        """
        starts the window and animation

        :return: None
        """

        self.frame()  # start the animation even if self.running is False
        self.root.mainloop()

    def destroy(self) -> None:
        """
        stops the app and quits

        :return: None
        """

        # close the window and set running to False
        self.root.destroy()
        self.running = False


if __name__ == '__main__':
    App().start()
