from chess import Board


class Bot:
    def __init__(self, game, stockfish=False):
        # either create a dataset of tagged positions or use reinforcement learning

        # for a dataset (supervised learning):
        #     1. learn to use the chess.com/lichess/stockfish api
        #     2. randomly choose a position and query the api for the evaluation of the position
        #     3. add that score to a dataframe with some representation of the board
        #     4. either use a neural network or some weird classifier

        # for reinforcement learning (unsupervised learning):
        #     1. learn how to use either deep q learning or find a different model type
        #     2. functions and methods to play the game on its own
        #     3. decide a scoring metric (maybe reward/penalties for captures and checkmate)

        # then:
        # find a way to store the model (pickling?)
        # create and train said model
        # find a way to play against it

        self.game = game
        self.model = None  # TODO: actually make a bot ?!?!?1
        self.stockfish = False
        self.moves = {}

    def move(self):
        # do something
        if self.game.game_over:
            # do something else
            pass

    def get_moves(self):
        if self.game.check[self.game.turn]:
            self.moves = dict(self.game.check_moves)
            return
        for row in self.game.array:
            for piece in row:
                if piece is None:
                    continue
                c = (piece.row, piece.col)
                self.moves[c] = piece.get_moves


def start():
    g = Board()
    bot = Bot(g)
    # TODO: something idfk


if __name__ == '__main__':
    start()
