"""
  triple2DTM.py
  convert triple to DTM matrix
"""

import glob
import time
import re
import txt2list
import numpy as np


def main():
    flog = open('../DTMlog.txt', 'w+', encoding='utf-8')

    triple_list = glob.glob('../triple/IS*.txt')

    for triple in triple_list:
        input_file = triple
        file_name = re.search('triple(.+?)-13-17.txt', triple).group(1)[1:]

        start = time.time()
        print("Generating {} DTM ... ".format(file_name), flush=False)

        file = txt2list.txt2list(input_file)
        lists = file.convert(",")


        term_list = []
        freq_list = []
        totalRows = lists.shape[0]
        d_size = int(lists[totalRows-1][0]) + 1
        dtm = np.zeros((d_size, 1), order="F")
        for d in range(d_size):
            for i in range(totalRows):
                t_size = len(term_list)
                record = lists[i]
                document = int(record[0])
                if document == d:
                    term = record[-1]
                    if t_size is 0:
                        term_list.append(term)
                        freq_list.append(1)
                        dtm[d][0] = 1
                        continue
                    elif term in term_list:
                        try:
                            index = term_list.index(term)
                            freq_list[index] += 1
                            # consider TF
                            # DTM[d][index] += 1
                            # without TF
                            dtm[d][index] = 1
                            continue
                        except:
                            print("Failed to add {} to {}".format(term, file_name))
                            raise
                    elif term not in term_list:
                        term_list.append(term)
                        freq_list.append(1)
                        # DTM = np.c_[DTM, np.zeros([D_size,1])]
                        # np.concatenate with axis is faster
                        dtm = np.concatenate((dtm, np.zeros((d_size,1))), axis=1)
                        dtm[d][t_size] = 1
                        continue
                else:
                    continue

        output_file = open("../DTM/{}.npy".format(file_name), 'wb+')
        np.save(output_file, dtm)
        output_file.close()

        term_file = open("../term/{}.txt".format(file_name), 'w+')
        term_size = len(term_list)
        freq_size = len(freq_list)
        if term_size == freq_size:
            for j in range(term_size):
                term_file.write("{}\t{}\n".format(term_list[j], str(freq_list[j])))
            term_file.close()
        else:
            print("Error: size of frequency list is not equal to term list")

        duration = float("{0:.2f}".format(time.time() - start))
        try:
            flog.write("{} \t {} \t {} \t {} \n".format(file_name, dtm.shape, totalRows, duration))
            print("finished in %f sec." % duration, flush=True)
        except Exception as e:
            print("Failed to log {}".format(file_name))
            raise

    flog.close()


if __name__ == '__main__':
    main()






