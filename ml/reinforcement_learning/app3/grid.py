from constants import *


class Grid:
    def __init__(self, parent, canvas, size, start, goal, blocks, walls,
                 mouse_handler):
        self.parent = parent
        self.size = size

        self.start, self.goal = start, goal
        self.walls, self.blocks = walls, blocks

        self.mouse = mouse_handler

        self.canvas = self.create_canvas(canvas)
        self.showing_moves, self.showing_numbers = False, False
        self.draw_grid()

    def create_canvas(self, canvas):
        dim = self.size * Constants.size

        canvas.configure(width=dim, height=dim, background=Constants.bg)
        canvas.grid(row=0, column=0, rowspan=5)

        canvas.bind('<ButtonPress>', lambda e: self.mouse(e.num, True, e.x, e.y))
        canvas.bind('<Motion>', lambda e: self.mouse(-1, None, None, None))
        canvas.bind('<ButtonRelease>', lambda e: self.mouse(e.num, False, e.x, e.y))

        return canvas

    def draw_grid(self):
        def color(k):
            if k in self.blocks:
                return Constants.block_color
            if k == self.start:
                return Constants.start_color
            return Constants.goal_color if k == self.goal else Constants.bg

        self.delete('all')

        pos = y = 0
        for _ in range(self.size):
            y1, x = y + Constants.size, 0
            for _ in range(self.size):
                x1 = x + Constants.size
                self.canvas.create_rectangle(x, y, x1, y1,
                                             fill=color(pos), outline=Constants.grid_color, tags=(f'loc_{pos}',))
                x = x1
                pos += 1
            y = y1

        for a, b in self.walls:
            inter = intersection(self.size, a, b)
            if len(inter) != 2:
                print(f'{a} and {b} were not adjacent')
                continue
            a_p, b_p = inter
            self.canvas.create_line(*a_p, *b_p, fill=Constants.wall_color, width=Constants.wall_width,
                                    tags=(f'wall_{a}x{b}', f'wall_{b}x{a}'))

    def change_color(self, k, color):
        self.canvas.itemconfigure(f'loc_{k}', fill=color)

    def delete(self, tag):
        self.canvas.delete(tag)

    def get_moves(self, r, c):
        k = flatten(self.size, r, c)
        for move in list(adjacent(self.size, k)):
            if move in self.blocks:
                continue
            if (k, move) in self.walls or (move, k) in self.walls:
                continue
            yield move
        yield k

    def draw_nums(self):
        for r in range(self.size):
            for c in range(self.size):
                self.canvas.create_text((c + 0.5) * Constants.size, (r + 0.5) * Constants.size, text=str(r * self.size + c),
                                        font=('Arial', 20), fill='#444444', tags=('numbers',))

    def show_moves(self):
        r, c = (max(0, self.canvas.winfo_pointery() - self.canvas.winfo_rooty()) // Constants.size,
                max(0, self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()) // Constants.size)
        for j in self.get_moves(r, c):
            r1, c1 = divmod(j, self.size)
            self.canvas.create_rectangle(c1 * Constants.size, r1 * Constants.size, c1 * Constants.size + Constants.size, r1 * Constants.size + Constants.size,
                                         fill='blue', tags=('moves',))

    def reset_drawings(self):
        if self.showing_moves:
            self.delete('moves')
            self.show_moves()

    def reset_obstacles(self):
        self.walls, self.blocks = [], []
        self.draw_grid()

    def iterate_pos(self, k):
        if k in self.blocks:
            return

        if k == self.start:
            if self.goal is not None:
                self.change_color(self.goal, Constants.bg)
            self.start, self.goal, color = None, self.start, Constants.goal_color
        elif k == self.goal:
            self.goal, color = None, Constants.bg
        else:
            if self.start is not None:
                self.change_color(self.start, Constants.bg)
            self.start, color = k, Constants.start_color
        self.change_color(k, color)

    def create_block(self, k):
        if k in (self.start, self.goal):
            return

        if k in self.blocks:
            self.blocks.remove(k)
            self.change_color(k, Constants.bg)
            return

        self.change_color(k, Constants.block_color)
        self.blocks.append(k)

    def create_wall(self, a, b):
        if (a, b) in self.walls:
            self.walls.remove((a, b))
            self.delete(f'wall_{a}x{b}')
            return
        elif (b, a) in self.walls:
            self.walls.remove((b, a))
            self.delete(f'wall_{b}x{a}')
            return

        inter = intersection(self.size, a, b)

        if len(inter) != 2:
            print(f'{a} and {b} were not adjacent')
            return

        a_p, b_p = inter
        self.canvas.create_line(*a_p, *b_p, fill=Constants.wall_color, width=Constants.wall_width,
                                tags=(f'wall_{a}x{b}', f'wall_{b}x{a}'))
        self.walls.append((a, b))

    def change_size(self, size, align: -1 | 1 = 1):
        diff = size - self.size

        def bounds(k):
            if k is None:
                return True

            r, c = divmod(k, self.size)
            if r >= size:
                return False
            return c < size if align == 1 else c > (1 - diff)

        def reformat(iterable):
            return [k if k is None else (k + diff * (k // self.size + (align == -1))) for k in iterable]

        def trim(iterable, strict=False):
            return reformat([k for k in iterable if bounds(k)] if strict else
                            [k if bounds(k) else None for k in iterable])

        if diff > 0:
            self.blocks = reformat(self.blocks)
            self.walls = list(map(reformat, self.walls))

            self.start, self.goal = reformat([self.start, self.goal])
        elif diff < 0:
            self.blocks = trim(self.blocks)
            self.walls = [reformat(wall) for wall in self.walls if len(trim(wall, strict=True)) == 2]

            self.start, self.goal = trim([self.start, self.goal], strict=False)

        dim = size * Constants.size
        self.canvas.configure(width=dim, height=dim)
        self.canvas.winfo_parent().geometry(f'{dim + Constants.size}x{dim}')

        self.size = self.parent.size = size
        self.draw_grid()

    def get_legality_matrix(self):
        s2 = self.size * self.size

        arr = []
        for state in range(s2):
            moves = list(adjacent(self.size, state)) + [state]
            arr.append([int(i in moves) for i in range(s2)])

        arr = np.array(arr)
        arr[:, self.goal] = Constants.goal

        for a, b in self.walls:
            arr[a, b] = 0
            arr[b, a] = 0

        for block in self.blocks:
            arr[block] = 0
            arr[:, block] = 0

        return arr
