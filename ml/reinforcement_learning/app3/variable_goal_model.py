from constants import *
from model import Model


class VariableGoalModel(Model):
    def reset(self):
        self.goal.reset()
        self.state = self.start

    def get_moves(self, state):
        return list(filter(lambda a: a[1] != Constants.illegal,
                           [(i, self.reward(state, i, self.goal)) for i in self.states]))

    def choose_action(self, state):
        if uniform(0, 1) < self.exploration:
            actions = self.get_moves(state)
            return choice(actions) if actions else (-1, Constants.illegal)

        moves = [(i, self.reward(state, i, self.goal)) for i in range(self.states_n)]
        return max(moves, key=lambda a: Constants.illegal if a[1] == Constants.illegal else self.Q[state, a[0]])

    def step(self, action, training=False, illegal_moves=False):
        reward = self.reward(self.state, action, self.goal)
        if training:
            self.update_q(self.state, action, reward)
        if reward != Constants.illegal or illegal_moves:
            self.state = action
            if action == self.goal:
                self.goal.next()

        return reward, self.state == self.goal
