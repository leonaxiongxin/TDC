import numpy as np


class NPY2CSV:
    def __init__(self, input_file, output_file, encoding='utf-8'):
        """
        @description: Initialize the class with the paths to the input txt file
        @param input_file: input npy file pathname
        @param output_file: output txt file pathname
        @param encoding: default to encode output file with utf-8, gbk is preferred when Chinese is included
        """
        self.nd_array = np.load(input_file)

        try:
            self.output = open(output_file, 'w+', encoding=encoding)
        except Exception:
            print("Failed to open the %s", output_file)
            raise

    def convert(self, header, fmt, delimiter=','):
        """
        @description: Convert the npy file to csv file
        @param header: header list in csv file, default to be null when it is not given
        @param fmt: field format for the csv file
        @param delimiter: csv field delimiter, default to use comma
        @return: csv file
        """
        if header:
            header_size = len(header)
            for i in range(header_size - 1):
                self.output.write('{},'.format(header[i]))
            self.output.write('{}\n'.format(header[header_size - 1]))
        else:
            pass
        np.savetxt(self.output, self.nd_array, fmt=fmt, delimiter=delimiter, newline='\n')
        self.output.close()


# file_name = 'IS-tdc-13-17'
file_name = 'IS-CS-MS-tdc-17'
file_input = '../data/tdc/{}.npy'.format(file_name)
file_output = '../data/tdc/{}.txt'.format(file_name)
file_header = ['tdc']
file_fmt = '%.7f'

file = NPY2CSV(file_input, file_output, 'gbk')
file.convert(file_header, file_fmt)
