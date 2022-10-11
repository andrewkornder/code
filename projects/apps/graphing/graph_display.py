import tkinter
import equation_processing as eq


size = 800
origin = 400
x_axis_height = size - 100
height = 10
line_color = 'red'
background = 'black'
circle_size = 10, 8
scale = 50


def blank_graph(window):
    window.delete('all')

    window.create_line((origin, 0), (origin, size), fill='white')
    window.create_line((0, x_axis_height), (size, x_axis_height), fill='white')


def create_graph(window, equation):
    blank_graph(window)

    last = 0, x_axis_height - eq.solve(equation, -origin)
    window.create_oval(*last, *last, fill='white', outline='')
    fails = []
    for x in range(1, size * scale):
        x = x / scale
        try:
            y = eq.solve(equation, x - origin)
        except ArithmeticError:
            fails.append((x, last[1]))
        else:
            y1 = x_axis_height - y
            window.create_oval(*get_circle(x, y1, 2), fill=line_color, outline='')
            last = x, y1

    [failed_plot(window, p) for p in fails]


def get_circle(x, y, r):
    return x - r, y - r, x + r, y + r


def failed_plot(window, point):
    window.create_oval(*get_circle(*point, circle_size[0]), fill=line_color, outline='')
    window.create_oval(*get_circle(*point, circle_size[1]), fill=background, outline='')


root = tkinter.Tk()
root.configure(bg='black')
root.geometry('%sx%s' % (size + 100, size))

canvas = tkinter.Canvas(root, bg=background, width=size, height=size)
canvas.grid(row=0, column=0)

entry = tkinter.Entry(root)
entry.grid(row=0, column=1)

root.bind('<Return>', lambda e: create_graph(canvas, entry.get()))
root.mainloop()
