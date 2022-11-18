from itertools import product


class Bot:
    @staticmethod
    def test_equation(equation):
        rhs, lhs = equation.split('=')
        if any(a * 2 in equation for a in '+-/=*'):
            return False
        if any('/0' in x or not x or x in '-+=*/' for x in (rhs, lhs)):
            return False
        try:
            exec(f'1 / (({lhs}) - ({rhs}))')
        except ZeroDivisionError:
            return True
        except Exception:
            return False
        return False

    @staticmethod
    def get_permutations(length):
        """
        a valid equation will always have the lhs and right hand side equal, so lhs - rhs will be 0
        we can exploit this to get an error when running exec(" 1 / (lhs - rhs) "),
        this way we dont have to code a parser for math eq

        a valid solution will have all operations on the lhs, so we remove those to filter for solutions only
        """

        eq = product('1234567890-+*/=', repeat=length)
        for string in eq:
            string = ''.join(string)
            if len(string.split('=')) != 2:
                continue
            if not Bot.test_equation(string):
                continue
            if any(x in string.split('=')[1] for x in '-+/*'):
                continue

            yield string

        return None

    def __init__(self, length):
        if type(length) == list:
            self.answers = length
        else:
            self.answers = self.get_permutations(length)
        self.random_threshold = 3
        print(self.answers)

        from random import choice
        self.best = ''  # random for speed, find later
        print('finished getting answers')

        r = 1
        while True:  # TODO: make a gui
            guess, result = (lambda a: (*a,) + tuple([''] * (2 - len(a))) if len(a) != 2 else a)(input('guess? (leave blank for best choice): ').split())
            if guess == 'gg':
                break

            print(guess, result)
            if not result:
                print(f'using {(self.best, result)} as guess')
                guess, result = self.best, guess

            self.answers = self.eliminate_guesses(guess, list(map(int, result)))

            self.score_guesses()

            self.best = self.answers[0]
            print(f'best guess: "{self.best}" ({", ".join(self.answers[:3])})\nremaining: {len(self.answers)}')

    def eliminate_guesses(self, guess, result, l=None):  # use a min-max like search, cancel out by first to last
        return [a for a in (self.answers if not l else l) if self.get_output(guess, a) == result]

    def score_guesses(self):
        scores = {}
        length = len(self.answers)
        for guess in self.answers:
            scores[guess] = sum(len(self.eliminate_guesses(guess, self.get_output(guess, ans))) - length for ans in self.answers)
        self.answers = sorted(self.answers, key=lambda x: scores[x])

    @staticmethod
    def get_output(guess, answer):
        r, answer = [0] * len(guess), list(answer)

        for i, (gl, al) in enumerate(zip(guess, answer)):
            if gl == al:
                r[i] = 2
                answer[i] = ''

        for i, l in enumerate(guess):
            if not answer[i]:
                continue

            if l in answer:
                r[i] = 1
                answer[answer.index(l)] = ''
            else:
                r[i] = 0
        return r


if __name__ == '__main__':
    Bot(8)
