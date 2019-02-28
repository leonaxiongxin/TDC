"""
  txt2list.py
  convert text file to python list
"""

import numpy as np


class txt2list:

    def __init__(self, input_file):
        """Initialize the class with the paths to the input txt file
        Keyword arguments:
        input_file -- input xml filename
        """

        # open the txt file for iteration
        self.context = self.readFile(input_file)

    def readFile(self, fileName):
        with open(fileName, 'rb') as f:
            # Generator without storage
            # lines = (line.strip() for line in f)
            return f.readlines()

    def convert(self, delimiter, noheader=False):
        """Convert the txt file to iterating list
            Keyword arguments:
            delimiter -- csv field delimiter
            noheader -- is there header in csv file
            Returns:
            numpy list,
        """
        first_row = self.context[0]
        headers = first_row.decode('UTF-8').split(delimiter)

        if noheader:
            lines = self.context
        else:
            lines = self.context[1:]

        size = len(headers)
        length = len(lines)
        lists = []

        for i in range(length):
            record = []
            line = lines[i].strip()
            elements = line.decode('UTF-8').split(delimiter)
            if len(elements) == size:
                for j in range(size):
                    record.append(elements[j].strip())
            else:
                # print(len(elements), size, elements)
                continue
            lists.append(record)

        result = np.array(lists)
        # print(result.shape)
        return result
