from constants import *


class Apple:
    def __init__(self, snake, size, locations):
        self.snake = snake
        self.locations = locations
        self.i = 0
        self.size = size
        self.s2 = size * size

        self.loc = None
        self.next()

    def __divmod__(self, other):
        return divmod(self.loc, other)

    def set_size(self, size, align):
        diff = size - self.size

        if diff > 0:
            self.loc = self.loc + diff * (self.loc // self.size + (align == -1))
        elif diff < 0:
            r, c = divmod(self.loc, self.size)
            if r >= size or not (c < size if align == 1 else c > (1 - diff)):
                self.next()

        self.size = size

    def reset(self):
        self.i = 0

    def next(self):
        if self.i < len(self.locations):
            self.loc = self.locations[self.i]
            self.i += 1
            return
        self.loc = choice([i for i in range(self.s2) if i not in self.snake.positions and i not in []])
