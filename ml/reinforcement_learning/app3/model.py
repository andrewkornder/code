from constants import *

from random import uniform
from functools import cache


class Model:
    step_size = Constants.alpha
    decay = Constants.gamma
    exploration = Constants.epsilon

    def __init__(self, total_states, total_actions, available_states, reward, start, goal,
                 record_interval=None, training_type='random'):
        self.reward = reward

        self.states = available_states
        self.states_n, self.actions_n = total_states, total_actions
        self.Q = np.zeros([self.states_n, self.actions_n])

        self.start, self.goal = start, goal
        self.state = start

        self.record = {}

        if record_interval is not None:
            self.record_training = max(0, record_interval)
        else:
            self.record_training = Constants.record_int

        self.train = lambda rounds, func=getattr(self, 'train_' + training_type): func(rounds)

    def get_moves(self, state):
        return list(filter(lambda a: a[1] != Constants.illegal, [(i, self.reward(state, i)) for i in self.states]))

    def choose_action(self, state):
        if uniform(0, 1) < self.exploration:
            actions = self.get_moves(state)
            return choice(actions) if actions else (-1, Constants.illegal)

        moves = [(i, self.reward(state, i)) for i in range(self.states_n)]
        return max(moves, key=lambda a: Constants.illegal if a[1] == Constants.illegal else self.Q[state, a[0]])

    def step(self, action, training=False, illegal_moves=False):
        reward = self.reward(self.state, action)
        if training:
            self.update_q(self.state, action, reward)
        if reward > 0 or illegal_moves:
            self.state = action

        return reward, self.state == self.goal

    def update_q(self, state, action, reward):
        self.Q[state, action] += self.step_size * (reward - Constants.disincentive +
                                                   self.decay * np.max(self.Q[action, ]) - self.Q[state, action])
        
    def update_q_b(self, state, action, reward):
        self.Q[state, action] += self.step_size * (reward + self.decay * np.max(self.Q[action, ])
                                                   - self.Q[state, action])
        
    def train_games(self, rounds):
        for rnd in range(rounds):
            self.start_round(rnd)
            self.reset()
                
            for current_turn in range(Constants.max_plays):  # play game
                seed = self.Q[self.state, ] + np.random.randn(1, self.actions_n) * (1 / (2 * rnd + 2))
                action = np.argmax(seed)
                reward, finished = self.step(action, training=True)

                if finished:
                    if Constants.progress:
                        print(f'\nfinished round {rnd} in {current_turn} turns')
                    break
        return self

    def train_pure_random(self, rounds):
        for rnd in range(rounds):
            self.start_round(rnd)

            state = choice(self.states)
            actions = self.get_moves(state)
            if not actions:
                continue

            self.update_q(state, *choice(actions))
        return self

    def train_pseudorandom(self, rounds):
        for rnd in range(rounds):
            self.start_round(rnd)
            if Constants.progress:
                print(f'\r{rnd:>10}', end='')

            state = choice(self.states)
            self.update_q(state, *self.choose_action(state))
        return self

    def start_round(self, i):
        if Constants.progress:
            print(f'\r{i:>10}', end='')
            
        if self.record_training != 0 and i % self.record_training == 0:
            self.record[i] = self.play_game()
            
    def reset(self):
        self.state = self.start

    def play_game(self):
        self.reset()

        record = [self.state]
        for _ in range(Constants.max_plays):
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
    def from_grid(cls, grid, **kwargs):
        n, blocks, walls, start, goal = grid.size, grid.blocks, grid.walls, grid.start, grid.goal

        @cache
        def reward(state, action):
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

        return cls(n * n, n * n, [i for i in range(n * n) if i not in blocks], reward, start, goal, **kwargs)
