import csv


class CSVWriter:

    def __init__(self, file_path, delimiter = ','):
        self.file_path = file_path
        self.delimiter = delimiter
        self.file = None
        self.writer = None


    def open(self):
        self.file = open(self.file_path, 'w')
        self.writer = csv.writer(self.file, delimiter = self.delimiter)


    def close(self):
        self.file.close()


    def write_row(self, row):
        self.writer.writerow(row)


    def write_rows(self, rows):
        for row in rows:
            self.write_row(row)