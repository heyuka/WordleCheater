import csv


class CSVToList:
    """Import data from a .csv file and return it as a list of lists."""
    def __init__(self, filename):
        self.list = []
        with open(filename, 'r') as csv_file:
            read_csv = csv.reader(
                csv_file,
                delimiter=',',
                quoting=csv.QUOTE_NONNUMERIC
            )
            for line in read_csv:
                for element in line:
                    self.list.append(element)
