import numpy as np
from random import choice, uniform
from functools import cache
from app3 import App, PathDisplay, GOAL
from pprint import pprint


ROUNDS = 10 ** 5
MAX_PLAYS = 25
TRAINING_TYPE = 1
PROGRESS = False

ILLEGAL = -100
POSITIVE = 10
NEGATIVE = -10
DISINCENTIVE = 10
ALLOW_STANDING = False


def manhattan_dist(a, b):
    return sum(abs(a_i - b_i) for a_i, b_i in zip(a, b))


class Model:
    step_size = 1
    decay = 0.75
    exploration = 0.3

    def __init__(self, total_states, total_actions, available_states, reward, start, goal,
                 record_interval=0, training_type=1):
        self.reward = reward

        self.states = available_states
        self.states_n, self.actions_n = total_states, total_actions
        self.Q = np.zeros([self.states_n, self.actions_n])

        self.start, self.goal = start, goal
        self.state = start

        self.record = {}
        self.record_training = max(0, record_interval)

        self.train = lambda rounds, func=getattr(self, 'train_' + chr(65 + training_type)): func(rounds)

    def get_moves(self, state):
        return list(filter(lambda a: a[1] > 0, [(i, self.reward(state, i)) for i in self.states]))

    def choose_action(self, state):
        if uniform(0, 1) < self.exploration:
            actions = self.get_moves(state)
            if actions:
                return choice(actions)

        action = np.argmax(self.Q[state, ])  # TODO: should be only legal entries in the Q arr
        return action, self.reward(state, action)

    def step(self, action, training=False, illegal_moves=False):
        reward = self.reward(self.state, action)
        if training:
            self.update_Q(self.state, action, reward)
        if reward > 0 or illegal_moves:
            self.state = action

        return reward, self.state == self.goal

    def update_Q(self, state, action, reward):
        self.Q[state, action] += self.step_size * (reward - DISINCENTIVE + self.decay * np.max(self.Q[action, ])
                                                   - self.Q[state, action])
        
    def update_Q_B(self, state, action, reward):
        self.Q[state, action] += self.step_size * (reward + self.decay * np.max(self.Q[action, ])
                                                   - self.Q[state, action])
        
    def train_A(self, rounds):
        for rnd in range(rounds):
            self.reset()

            if PROGRESS:
                print(f'\r{rnd:>10}', end='')
                
            for current_turn in range(MAX_PLAYS):  # play game
                seed = self.Q[self.state, ] + np.random.randn(1, self.actions_n) * (1 / (2 * rnd + 2))
                action = np.argmax(seed)
                reward, finished = self.step(action, training=True)

                if finished:
                    if PROGRESS:
                        print(f'finished round {rnd} in {current_turn} turns')
                    break

            if self.record_training != 0 and rnd % self.record_training == 0:
                self.record[rnd] = self.play_game()

    def train_B(self, rounds):
        for rnd in range(rounds):
            if PROGRESS:
                print(f'\r{rnd:>10}', end='')

            state = choice(self.states)
            actions = self.get_moves(state)
            if not actions:
                continue

            action, reward = choice(actions)

            self.update_Q(state, action, reward)

    def train_C(self, rounds):
        for rnd in range(rounds):
            if PROGRESS:
                print(f'\r{rnd:>10}', end='')

            state = choice(self.states)
            self.update_Q(state, *self.choose_action(state))

    def reset(self):
        self.state = self.start

    def play_game(self):
        self.reset()

        record = [self.state]
        for _ in range(MAX_PLAYS):
            reward, finished = self.step(np.argmax(self.Q[self.state, ]), illegal_moves=True)

            record.append(self.state)
            if finished:
                return record
        return record + [-1]


class PathFinderModel(Model):
    @classmethod
    def from_matrix(cls, matrix, start, goal, **kwargs):
        sn, an = matrix.shape
        return cls(sn, an, [i for i in range(sn) if any(x > 0 for x in matrix[i])],
                   cache(lambda s, a: matrix[s, a]), start, goal, **kwargs)

    @classmethod
    def from_grid(cls, n, walls, blocks, start, goal, **kwargs):
        @cache
        def reward(state, action):
            if not ALLOW_STANDING and state == action:
                return ILLEGAL

            if action in blocks or state in blocks:
                return ILLEGAL

            if (state, action) in walls or (action, state) in walls:
                return ILLEGAL

            s, a = divmod(state, n), divmod(action, n)
            legal = manhattan_dist(s, a) <= 1.0
            if not legal:
                return ILLEGAL

            if action == goal:
                return GOAL

            g = divmod(goal, n)
            return POSITIVE if manhattan_dist(a, g) < manhattan_dist(s, g) else NEGATIVE

        return cls(n * n, n * n, [i for i in range(n * n) if i not in blocks], reward, start, goal, **kwargs)


def create_model(self):
    if None in (self.start, self.goal):
        print(f'None appears >= 1 times in {(self.start, self.goal)}, both must be present to train the model')
        return

    rounds = int((lambda a, b: 10 ** float(a) if a.isdecimal() else b)(self.entry.get(), ROUNDS))
    model = PathFinderModel.from_grid(self.size, self.walls, self.blocks, self.start, self.goal,
                                      training_type=TRAINING_TYPE, record_interval=self.record_interval)

    print('training model for', rounds, 'rounds')
    model.train(rounds)

    pprint({k: v for k, v in model.record.items() if v[-1] != -1})

    path = model.play_game()
    if path[-1] == -1:
        path = path[:-1]

    state = model.start
    for action in path:
        print(f'{state} -> {action}: {model.reward(state, action)}')
        state = action

    draw_path(self, path)


def create_model_windowless(n, walls, blocks, start, goal, rounds):
    model = PathFinderModel.from_grid(n, walls, blocks, start, goal,
                                      training_type=TRAINING_TYPE, record_interval=5)
    model.train(10 ** rounds)

    # pprint({k: v for k, v in model.record.items() if v[-1] != -1})

    path = model.play_game()
    return path


def draw_path(self, path):
    self.canvas.delete('path')
    centers = np.array([np.array([sum(c) / 4 for c in zip(*self.bounding(k))]) for k in path])

    PathDisplay(centers, self.canvas, 'linear')
    PathDisplay(centers, self.canvas, 'interpolated', definition=self.size * self.size)


if __name__ == '__main__':
    model_type = 0
    TRAINING_TYPE = 2

    n = 5
    _blocks = [1 + i * (n + 1) for i in range(n - 1)] + \
              [-2 + i * (n + 1) for i in range(2, n)]

    App(n, blocks=_blocks, start=0, goal=n * n - 1, model=create_model, record=5).run(True)
