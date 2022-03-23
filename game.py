import numpy as np

from wordlist import Wordlist


class Game:
    def __init__(self, filename):
        self.words = Wordlist(filename).wordlist
        self.solution = np.random.choice(self.words)
        print(self.solution)

    def process_guess(self, guess):
        val = [0, 0, 0, 0, 0]

        for position, letter in enumerate(guess):
            for _letter in self.solution:
                if letter == _letter:
                    val[position] = 1

        for position, letter in enumerate(guess):
            if guess[position] == self.solution[position]:
                val[position] = 2

        return val
