import numpy as np
import re


def get_journals():
    with open('../data/journals_{}.txt'.format(FIELD), encoding='utf-8') as f:
        line = f.readline()
        journals_name = line.split(',')
        journals_path = []
        for journal in journals_name:
            journals_path.append("../data/term/{}.npy".format(journal))
        return journals_path


def main(npy_list):
    length = len(npy_list)

    for count in range(length):
        input_file = npy_list[count]
        file_name = re.search('{}-(.+?).npy'.format(FIELD), input_file).group(1)
        term_info = np.load(input_file)
        tdc_info = np.load("../data/TDC/{}-{}.npy".format(FIELD, file_name))
        # print(term_info[100])
        # print('\n')
        # print(term_info[0])

        output_file = open("../data/term/{}-{}.txt".format(FIELD, file_name), "w+", encoding="gbk")
        output_file.write('tdc,df,tf,tf2013,tf2014,tf2015,tf2016,tf2017,term\n')
        for i in range(len(tdc_info)):
            # term_info[i] = [term, df, tf, freq_by_pys]
            tdc = tdc_info[i]
            term = term_info[i][0]
            df = term_info[i][1]
            tf = term_info[i][2]
            pys = term_info[i][3]
            output_file.write('{:.7f},{},{},{},{}\n'.format(tdc, df, tf, pys, term))
        output_file.close()


if __name__ == '__main__':
    FIELD = "IS"
    target_files = get_journals()
    main(target_files)
