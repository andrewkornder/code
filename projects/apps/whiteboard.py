import tkinter as tk

color = 'black'
bg = 'white'

def switch(e):
	global press
	press = not press


def draw_line(coords):
	global last, drawing
	if not press:
		last = coords
		return
	drawing = canvas.create_line(last, coords, fill=color, width=5)
	last = coords

root = tk.Tk()

dim = 1920, 1080
root.geometry('{}x{}+0+0'.format(*dim))

canvas = tk.Canvas(root, height=dim[1], width=dim[0], bg=bg)
canvas.pack()

press = False
last = 0, 0

canvas.bind('<Motion>', lambda e: draw_line((e.x, e.y)))
canvas.bind('<ButtonPress>', switch)
canvas.bind('<ButtonRelease>', switch)

root.bind('<space>', lambda e: canvas.delete('all'))

root.mainloop()