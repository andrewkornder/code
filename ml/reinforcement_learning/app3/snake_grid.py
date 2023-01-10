from constants import *
from apple import Apple
from variable_goal_model import VariableGoalModel


class Snake:
    def __init__(self, grid, loc):
        self.grid = grid
        self.positions = [loc]

    @property
    def head(self):
        return self.positions[0]

    def step(self, pos):
        if pos == self.grid.apple:
            self.positions.insert(0, pos)
            return

        self.positions = [pos, *self.positions[:-1]]


class SnakeGrid:
    def __init__(self, parent, canvas, size, start, blocks, walls,
                 mouse_handler, apple_locations):
        self.parent = parent

        self.size = size
        self.snake = Snake(self, start)
        self.start, self.apple = start, Apple(**{'snake': self.snake, 'size': size, 'locations': apple_locations})
        self.blocks, self.walls = map(list, (blocks, walls))
        self.reward = get_variable_reward_func(size, walls, blocks)

        self.canvas = self.config_canvas(canvas, mouse_handler)

        self.showing_moves, self.showing_numbers = False, False
        self.draw_grid()

    def delete(self, *args): self.canvas.delete(*args)

    def change_color(self, k, color):
        self.canvas.itemconfigure(f'loc_{k}', fill=color)

    def config_canvas(self, canvas, on_mouse):
        dim = self.size * Constants.size

        canvas.configure(width=dim, height=dim, background=Constants.bg)
        canvas.grid(row=0, column=0, rowspan=5)

        canvas.bind('<ButtonPress>', lambda e: on_mouse(e.num, True, e.x, e.y))
        canvas.bind('<Motion>', lambda e: on_mouse(-1, None, None, None))
        canvas.bind('<ButtonRelease>', lambda e: on_mouse(e.num, False, e.x, e.y))

        return canvas

    def draw_grid(self):
        def color(k):
            if k in self.blocks:
                return Constants.block_color
            if k == self.start:
                return Constants.start_color
            return Constants.goal_color if k == self.apple else Constants.bg

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

    def draw_nums(self):
        for r in range(self.size):
            for c in range(self.size):
                self.canvas.create_text((c + 0.5) * Constants.size, (r + 0.5) * Constants.size, text=str(r * self.size + c),
                                        font=('Arial', 20), fill='#444444', tags=('numbers',))

    def show_moves(self):
        r, c = (max(0, self.canvas.winfo_pointery() - self.canvas.winfo_rooty()) // Constants.size,
                max(0, self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()) // Constants.size)
        k = r * self.size + c
        for j in adjacent(self.size, k):
            r1, c1 = divmod(j, self.size)
            self.canvas.create_rectangle(c1 * Constants.size, r1 * Constants.size,
                                         (c1 + 1) * Constants.size, (r1 + 1) * Constants.size,
                                         fill=Constants.gradient[self.reward(k, j, self.apple)], tags=('moves',))

    def reset_drawings(self):
        if self.showing_moves:
            self.delete('moves')
            self.show_moves()

    def reset_obstacles(self):
        self.walls, self.blocks = [], []
        self.draw_grid()

    def set_start(self, k):
        if k == self.apple:
            return

        if k in self.blocks:
            return

        if k == self.start:
            self.start = None
            self.change_color(k, Constants.bg)
            return

        self.start = k
        self.change_color(k, Constants.start_color)

    def create_block(self, k):
        if k in (self.start, self.apple):
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

            self.start = reformat([self.start])
        elif diff < 0:
            self.blocks = trim(self.blocks)
            self.walls = [reformat(wall) for wall in self.walls if len(trim(wall, strict=True)) == 2]

            self.start = trim([self.start], strict=False)

        dim = size * Constants.size
        self.canvas.configure(width=dim, height=dim)
        self.canvas.master.geometry(f'{dim + Constants.size}x{dim}')

        self.size = self.parent.size = size
        self.apple.set_size(size, align)

        self.draw_grid()


class SnakeModel(VariableGoalModel):
    @classmethod
    def from_grid(cls, grid, reward, **kwargs):
        n, blocks, walls, start, goal = grid.size * grid.size, grid.blocks, grid.walls, grid.start, grid.apple
        return cls(n, n, [i for i in range(n) if i not in blocks],
                   reward, start, goal, **kwargs)
