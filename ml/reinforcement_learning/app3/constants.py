from random import choice
import numpy
import pprint
import time


from colorsys import hsv_to_rgb
from math import exp


np = numpy
pprint = pprint.pprint
choice = choice
perf_counter = time.perf_counter


def _create_gradient(v, _r):
    _color_scale = lambda x: (2 + 1 / (1 + exp(16 * x / _r))) / 3
    _color_code = lambda x: map(lambda c: int(255 * c), hsv_to_rgb(_color_scale(x), 1, 1))
    return {x: (lambda r, g, b: f'#{r:02x}{g:02x}{b:02x}')(*_color_code(x)) for x in v}


class Constants:
    # window constants
    size = 100

    walk_color = 'blue'
    walk_time = 1.5

    wall_width = 6

    bg = 'white'
    block_color = '#333333'
    wall_color = '#333333'
    goal_color = 'green'
    start_color = 'red'
    grid_color = ''

    # model constants
    default_rounds = 3
    max_plays = 25
    record_int = 5
    training_options = 'games', 'pure_random', 'pseudorandom'
    progress = False
    allow_standing = False

    alpha = 0.25
    gamma = 0.9
    epsilon = 0.1

    illegal = -64
    positive = 8
    negative = -8
    goal = 64

    disincentive = 8

    score_values = goal, positive, negative, illegal
    lowest, highest = min(score_values), max(score_values)
    score_range = highest - lowest

    gradient = _create_gradient(score_values, score_range)

    @classmethod
    def set_hyper_params(cls, alpha, gamma, epsilon):
        cls.alpha = alpha
        cls.gamma = gamma
        cls.epsilon = epsilon


def manhattan_dist(a, b):
    return sum(abs(a_i - b_i) for a_i, b_i in zip(a, b))


def flatten(size, r, c):
    return r * size + c


def adjacent(size, k):
    r, c = divmod(k, size)
    if r != 0:
        yield k - size
    if r != size - 1:
        yield k + size
    if c != 0:
        yield k - 1
    if c != size - 1:
        yield k + 1


def bounding(r, c):
    return [((c + a) * Constants.size, (r + b) * Constants.size) for a in range(2) for b in range(2)]


def intersection(size, a, b):
    return set(bounding(*divmod(a, size))).intersection(bounding(*divmod(b, size)))
