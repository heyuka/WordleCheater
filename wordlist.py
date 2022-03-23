import csv
import numpy as np


class Wordlist:
    def __init__(self, filename):
        self.wordlist = []
        with open(filename, 'r') as csv_file:
            read_csv = csv.reader(
                csv_file,
                delimiter=',',
                quoting=csv.QUOTE_NONNUMERIC
            )
            for line in read_csv:
                for element in line:
                    self.wordlist.append(element)
        self.wordlist = np.array(self.wordlist)
