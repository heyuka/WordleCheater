import numpy as np

from wordlist import Wordlist


def get_candidates(_words, _scores):
    num_words = 10
    if len(_words) < 10:
        num_words = (len(_words))
    indices = np.argpartition(_scores, (num_words * -1))[(num_words * -1):]
    ew = np.zeros((num_words, 2))
    for index in range(num_words):
        ew[index][0] = indices[index]
        ew[index][1] = _scores[index]
    ew = np.sort(ew)
    for index in range(num_words):
        indices[index] = ew[index][0]
    top5 = _words[indices]
    top5 = top5[::-1]
    out = ""
    for word in top5:
        out += f" {word}"
    return out


class Cheater:
    def __init__(self, filename):
        self.guessed = []
        self.clean_words = Wordlist(filename).wordlist
        self.salty_words = Wordlist(filename).wordlist

        self.counts = np.zeros(26)
        for word in self.clean_words:
            for letter in word:
                self.counts[ord(letter) - 65] += 1

        counts_by_position = np.zeros((26, 5))
        for word in self.clean_words:
            for position, letter in enumerate(word):
                counts_by_position[ord(letter) - 65][position] += 1

        medians = np.median(counts_by_position, axis=0)

        scores_by_pos = np.zeros((26, 5))
        for i in range(len(scores_by_pos)):
            for j in range(len(scores_by_pos[i])):
                scores_by_pos[i][j] = counts_by_position[i][j] / medians[j]

        self.scores = np.zeros(len(self.clean_words))
        for i in range(len(self.clean_words)):
            word = self.clean_words[i]
            for position, letter in enumerate(word):
                self.scores[i] += scores_by_pos[ord(letter) - 65][position]
        self.salty_scores = np.copy(self.scores)

    def get_clean_candidates(self):
        doomed = []
        for word in self.clean_words:
            for letter in word:
                if word.count(letter) > 1:
                    doomed.append(np.where(self.clean_words == word))
                    break
        words = np.delete(self.clean_words, doomed)
        scores = np.delete(self.scores, doomed)
        return get_candidates(words, scores)

    def get_salty_candidates(self):
        doomed = []
        for word in self.salty_words:
            for guess in self.guessed:
                if word.count(guess) > 0:
                    doomed.append(np.where(self.salty_words == word))
                    break
        words = np.delete(self.salty_words, doomed)
        scores = np.delete(self.salty_scores, doomed)

        doomed = []
        for word in words:
            for letter in word:
                if word.count(letter) > 1:
                    doomed.append(np.where(words == word))
                    break
        words = np.delete(words, doomed)
        scores = np.delete(scores, doomed)
        return get_candidates(words, scores)

    def print_status(self):
        print(str(len(self.clean_words)) + " possible words remain")
        a = get_candidates(self.clean_words, self.scores)
        b = self.get_clean_candidates()
        c = self.get_salty_candidates()
        d = ""
        print(f"Most likely: {a}")
        print(f"No doubles: {b}")
        print(f"New letters: {c}")
        if len(c) > 1:
            d = c[:6]
        elif len(b) > 1:
            d = b[:6]
        elif len(a) > 1:
            d = a[:6]
        print(f"Best guess: {d}")

    def rule_out_letter(self, letter):
        self.guessed.append(letter)

        doomed = []
        for word in self.clean_words:
            if word.count(letter) > 0:
                doomed.append(np.where(self.clean_words == word))
        self.clean_words = np.delete(self.clean_words, doomed)
        self.scores = np.delete(self.scores, doomed)

        salty_doom = []
        for word in self.salty_words:
            if word.count(letter) > 0:
                salty_doom.append(np.where(self.salty_words == word))
        self.salty_words = np.delete(self.salty_words, salty_doom)
        self.salty_scores = np.delete(self.salty_scores, salty_doom)

    def require_letter(self, letter):
        self.guessed.append(letter)
        doomed = []
        for word in self.clean_words:
            if word.count(letter) == 0:
                doomed.append(np.where(self.clean_words == word))
        self.clean_words = np.delete(self.clean_words, doomed)
        self.scores = np.delete(self.scores, doomed)

    def rule_out_letter_at_position(self, letter, position):
        self.guessed.append(letter)

        doomed = []
        for word in self.clean_words:
            if word[position] == letter:
                doomed.append(np.where(self.clean_words == word))
        self.clean_words = np.delete(self.clean_words, doomed)
        self.scores = np.delete(self.scores, doomed)

        salty_doom = []
        for word in self.salty_words:
            if word[position] == letter:
                salty_doom.append(np.where(self.salty_words == word))
        self.salty_words = np.delete(self.salty_words, salty_doom)
        self.salty_scores = np.delete(self.salty_scores, salty_doom)

    def require_letter_at_position(self, letter, position):
        self.guessed.append(letter)
        doomed = []
        for word in self.clean_words:
            if word[position] != letter:
                doomed.append(np.where(self.clean_words == word))
        self.clean_words = np.delete(self.clean_words, doomed)
        self.scores = np.delete(self.scores, doomed)
