from constants import *

from app import App
from model import PathFinderModel
from path_display import PathDisplay
from gridsearch import GridSearch


class Maze(App):
    def __init__(self, n, blocks=(), walls=(), start=0, goal=None, training=0):
        super().__init__(n, start=start, goal=n * n - 1 if goal is None else goal,
                         blocks=blocks, walls=walls, training=training)

    def model(self):
        if None in (self.grid.goal, self.grid.start):
            return

        rounds = self.get_rounds()
        model = PathFinderModel.from_grid(self.grid, training_type=Constants.training_options[self.training]
                                          ).train(rounds)

        unique_paths = {}
        for i, path in model.record.items():
            path = tuple(path)
            if path not in unique_paths:
                unique_paths[path] = i

        path = tuple(model.play_game())
        if path[-1] == -1:
            print('failed to find path')
            return

        if path in unique_paths:
            print(f'Model({Constants.training_options[self.training]}) converged after {unique_paths[tuple(path)]} '
                  f'rounds out of {rounds} with a score of '
                  f'{sum(model.reward(path[i], action) for i, action in enumerate(path[1:]))}')
    
        state, colors = path[0], []
        for action in path[1:]:
            reward = model.reward(state, action)
            state = action
            colors.append(Constants.gradient[reward])
    
        self.draw_path(path, colors)

    def draw_path(self, path, colors):
        self.grid.delete('path')
        centers = np.array([np.array([sum(c) / 4 for c in zip(*bounding(*divmod(k, self.size)))]) for k in path])

        PathDisplay(centers, self.grid.canvas, 'linear', palette=colors)
        PathDisplay(centers, self.grid.canvas, 'interpolated', definition=self.size * self.size)


if __name__ == '__main__':
    _n = 5
    _blocks = [1 + i * (_n + 1) for i in range(_n - 1)] + \
              [-2 + i * (_n + 1) for i in range(2, _n)]

    app = Maze(_n, blocks=_blocks, start=0, goal=_n * _n - 1)
    app.run(False)

    grid = app.grid

    _start = perf_counter()

    scores = GridSearch(alpha=(0, 1), gamma=(0, 1), epsilon=(0, 1), test_length=9, grid=grid
                               ).full_params(10 ** 3)

    params, score = max(scores.items(), key=lambda x: x[1])
    print('\nalpha = %s\ngamma = %s\nepsilon = %s\nbest model = %s' % params)
    print('converged at round {}\ntook {:.2f}s'.format(*score))

    print('time spent training models %s' % (perf_counter() - _start))

    pprint(scores)
    