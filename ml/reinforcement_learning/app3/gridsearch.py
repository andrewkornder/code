from constants import *
from model import PathFinderModel


class GridSearch:
    def __init__(self, test_length, alpha, gamma, epsilon, training, grid):
        self.length = test_length
        self.grid = grid

        self.alpha = np.linspace(*alpha, test_length)
        self.gamma = np.linspace(*gamma, test_length)
        self.epsilon = np.linspace(*epsilon, test_length)

        self._best_params = (None, (1 << 16,))
        self.training = training
        self._results = {}

    def model(self, rounds):
        return PathFinderModel.from_grid(self.grid, training_type=self.training).train(rounds)

    def full_params(self, rounds):
        scores = {}
        for training_type in Constants.training_options:
            self.training = training_type
            if training_type in ('pure_random', 'games'):
                e, self.epsilon = self.epsilon, (None,)
                r = self.hyper_params(rounds, _progress=len(scores))
                self.epsilon = e
            else:
                r = self.hyper_params(rounds, _progress=len(scores))
            scores.update(r)
        return scores

    def hyper_params(self, rounds, _progress=0):
        values = [(a, g, e, self.training) for a in self.alpha for g in self.gamma for e in self.epsilon]

        scores = {}
        for index, a_g_e_t in enumerate(values):
            print(f'\r{index + _progress:>10}', end='')
            Constants.set_hyper_params(*a_g_e_t[:-1])

            start = perf_counter()

            model = self.model(rounds)
            path0, record = model.play_game(), model.record

            t_time = perf_counter() - start

            if path0[-1] == -1:
                scores[a_g_e_t] = (rounds, t_time)
                continue

            for i, path in record.items():
                if path == path0:
                    scores[a_g_e_t] = (i, time)
                    break

        cb = min(scores.items(), key=lambda x: x[1])
        self._best_params = min((self._best_params, cb),
                                key=lambda x: x[1])
        return scores

    @property
    def best_params(self):
        return self._best_params
