from random import choice, randint
import numpy
import pprint
import time
from functools import cache
from random import uniform


from colorsys import hsv_to_rgb
from math import exp


np = numpy
pprint = pprint.pprint
choice, randint, uniform = choice, randint, uniform
perf_counter = time.perf_counter
cache = cache


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
    record_int = 1
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


def get_static_reward_func(n, walls, blocks, goal):
    _reward = get_variable_reward_func(n, walls, blocks)
    return lambda _s, _a: _reward(_s, _a, goal)


def get_variable_reward_func(n, walls, blocks):
    def _reward(state, action, goal):
        if not Constants.allow_standing and state == action:
            return Constants.illegal

        sa = state, action
        if any(block in sa for block in blocks):
            return Constants.illegal

        if sa in walls or (action, state) in walls:
            return Constants.illegal

        s, a = divmod(state, n), divmod(action, n)
        legal = manhattan_dist(s, a) == 1
        if not legal:
            return Constants.illegal

        if action == goal:
            return Constants.goal

        g = divmod(goal, n)
        return Constants.positive if manhattan_dist(a, g) < manhattan_dist(s, g) else Constants.negative

    return _reward
