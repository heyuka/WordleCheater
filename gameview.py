from game import Game
from colorama import init, Fore, Back, Style
import os

STATES = [
    f"{Style.BRIGHT}{Back.RED}{Fore.BLACK}",
    f"{Style.BRIGHT}{Back.YELLOW}{Fore.BLACK}",
    f"{Style.BRIGHT}{Back.GREEN}{Fore.BLACK}",
    f"{Style.BRIGHT}{Back.WHITE}{Fore.BLACK}",
    f"{Style.RESET_ALL}"
]


def print_output(guess, result):
    ret = ""
    score = 0
    for i, value in enumerate(result):
        ret += f"{STATES[value]} {guess[i]} {STATES[4]} "
        score += value
    return [ret, score]


def check_input():
    msg = ": "
    user_input = input(msg).upper()

    if len(user_input) != 5:
        print("guess must by five letters")
        check_input(g)

    for letter in user_input:
        if ord(letter) < 65 or ord(letter) > 90:
            print("guess must contain only letters")

    return user_input


class GameView:

    def __init__(self, filename):
        self.g = Game(filename)
        init(autoreset=True)
        self.guesses = []
        out = ""
        for i in range(5):
            out += STATES[3] + "   "
            out += STATES[4] + " "
        print(out)

    def initial_prompt(self):
        while True:
            guess = check_input()
            result = self.g.process_guess(guess)
            result = print_output(guess, result)
            print(result[0])
            if result[1] >= 10:
                break
        print("Success!")