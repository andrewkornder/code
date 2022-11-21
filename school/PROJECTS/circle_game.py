#!/usr/bin/python
# circle_game.py

__author__ = "Andrew Kornder"
__version__ = '1.0'

'''creates a playable game where the user clicks on circles to get points'''

import tkinter
import random as r
import math


def on_click(event):
    """
    checks the positions of the circles and cursor on click to see if the user hit one

    :param event: the automatically generated param which contains the values on the mouse click
    :return None:
    """

    correct = False
    global score, score_display
    global moving

    for i, center in enumerate(circles):
        d = math.dist((event.y, event.y), center[1])
        if d < 10:
            canvas.delete(center[0])
            score += 10 - int(d)
            correct = True
            break
    for i, center in enumerate(moving):
        d = math.dist((event.y, event.y), tuple(center[1]))
        if d < 20:
            del moving[i]
            canvas.delete(center[0])
            score += 40 - int(d)
            correct = True
            break
    if not correct:
        score -= 5
    canvas.delete(score_display)
    new_score_text = 'score: ' + str(score) if score > -1 else 'score: 0'
    score_display = canvas.create_text((60, 10), text=new_score_text,
                                       fill='white')
    if score < -5:
        canvas.delete('all')
        canvas.create_text((500, 500), text='YOU LOST',
                           font=('Verdana', 30, 'bold'), fill='red')


def move_circles():
    """
    updates the positions of the circles which are set to be moving
    and changes the color to fade into the background

    :return None:
    """

    global moving
    for i, c in enumerate(moving):
        circle, xy, m, frame = c
        canvas.delete(circle)
        if xy[0] > 900:
            m = -1
        elif xy[0] < 100:
            m = 1
        xy[0] += m * 1
        size = 10
        frame[0] += frame[1] * 1
        color = str(hex(250 - frame[0] * 5))[2:]
        if len(color) == 1:
            color += '0'
        color = '#' + color + '0000'
        if frame[0] == 1:
            frame[1] = 1
        if frame[0] == 50:
            frame[1] = -1
        moving[i] = [
            canvas.create_oval(xy[0] - size, xy[1] - size, xy[0] + size,
                               xy[1] + size, fill=color), xy, m, frame]


def create_circle():
    """
    creates circles which are either moving or static

    :return None:
    """

    global cycle
    if cycle == 100:
        cycle = 0
        if r.randint(0, 4) == 0:
            center = r.randint(50, 950), r.randint(50, 950)
            size = 10
            circles.append((canvas.create_oval(center[0] - size,
                                               center[1] - size,
                                               center[0] + size,
                                               center[1] + size, fill='green'),
                            center))
        else:
            center = [r.randint(50, 950), r.randint(50, 950)]
            size = 20
            moving.append([canvas.create_oval(center[0] - size,
                                              center[1] - size,
                                              center[0] + size,
                                              center[1] + size, fill='green'),
                           center, [1, -1][r.randint(0, 1)], [50, -1]])

    cycle += 1
    move_circles()
    root.after(10, create_circle)


def set_up():
    """
    creates the window and the global variables

    :return None:
    """

    global root, canvas, score, circles, score_display, moving, cycle
    cycle = 100
    circles = []
    moving = []
    root = tkinter.Tk()
    root.geometry('{0}x{0}'.format(1000))
    score = 0
    canvas = tkinter.Canvas(root, width=1000, height=1000, bg='black')
    score_display = canvas.create_text((60, 10), text='score: 0', fill='white')
    canvas.pack()
    create_circle()
    canvas.bind('<Button-1>', on_click)
    root.mainloop()


if __name__ == '__main__':
    set_up()
