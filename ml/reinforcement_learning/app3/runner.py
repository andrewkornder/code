from constants import *

from window import App
from model import PathFinderModel
from path_display import PathDisplay


class Maze(App):
    def __init__(self, n, blocks=(), walls=(), start=0, goal=None, training=0):
        super().__init__(n, start=start, goal=n * n - 1 if goal is None else goal,
                         blocks=blocks, walls=walls)

    def model(self):
        if None in (self.grid.start, self.grid.goal):
            print(f'None appears >= 1 times in {(self.grid.start, self.grid.goal)}, '
                  f'both must be present to train the model')
            return

        rounds = self.get_rounds()
        model = PathFinderModel.from_grid(self.grid, training_type=Constants.training_options[self.training],
                                          record_interval=Constants.record_int)
    
        print('training model for', rounds, 'rounds')
        model.train(rounds)
    
        path = model.play_game()
        if path[-1] == -1:
            print('failed to find path')
            return
    
        state, colors = path[0], []
        for action in path[1:]:
            reward = model.reward(state, action)
            print(f'{state} -> {action}: {reward}')
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

    Maze(_n, blocks=_blocks, start=0, goal=_n * _n - 1).run(False)
    