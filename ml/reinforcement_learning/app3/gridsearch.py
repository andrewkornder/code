from constants import *
from model import PathFinderModel


class GridSearch:
    def __init__(self, test_length, alpha, gamma, epsilon, **kwargs):
        self.length = test_length
        self.kwargs = kwargs

        self.alpha = np.linspace(*alpha, test_length)
        self.gamma = np.linspace(*gamma, test_length)
        self.epsilon = np.linspace(*epsilon, test_length)

    def model(self, rounds):
        return PathFinderModel.from_grid(**self.kwargs).train(rounds)

    def full_params(self, rounds, best_score_only=False):
        scores = {}
        for training_type in Constants.training_options:
            print(f'\n{training_type}')
            self.kwargs['training_type'] = training_type
            if training_type in ('pure_random', 'games'):
                e, self.epsilon = self.epsilon, (None,)
                params, score = self.hyper_params(rounds, True)
                self.epsilon = e
            else:
                params, score = self.hyper_params(rounds, True)

            scores[params + (training_type,)] = score

        if best_score_only:
            return min(scores.items(), key=lambda x: x[1])
        return scores

    def hyper_params(self, rounds, best_score_only=False):
        values = [(a, g, e) for a in self.alpha for g in self.gamma for e in self.epsilon]

        total, scores = len(values), {}
        for index, a_g_e in enumerate(values):
            print(f'\r{index:>10} / {total}', end='')
            Constants.set_hyper_params(*a_g_e)

            start = perf_counter()

            model = self.model(rounds)
            path0, record = model.play_game(), model.record

            time = perf_counter() - start

            if path0[-1] == -1:
                scores[a_g_e] = (rounds, time)
                continue

            for i, path in record.items():
                if path == path0:
                    scores[a_g_e] = (i, time)
                    break

        if best_score_only:
            return min(scores.items(), key=lambda x: x[1])
        return scores
