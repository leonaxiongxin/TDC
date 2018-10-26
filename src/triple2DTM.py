"""
  triple2DTM.py
  convert triple to DTM matrix
"""

import glob
import time
import re
import txt2list
import numpy as np


def getJournals():
    with open('../data/journals.txt', encoding='utf-8') as f:
        line = f.readline()
        return line.split(',')


def convert(records, documents, file_name):
    """
    :param records: two-dimensional numpy array
    :param file_name: string
    :return: array with two elements
    """
    records_size = len(records)
    documents_size = len(documents)

    term_list = []
    freq_py_list = []
    py_options = range(2013, 2018)
    dtm = np.zeros((documents_size, 1), order="F")
    for d in range(documents_size):
        document = int(documents[d])
        for i in range(records_size):
            record = records[i]
            term_size = len(term_list)
            bh = int(record[0])
            if bh == document:
                term = record[-1]
                py = int(record[1])
                py_index = py_options.index(py)
                if term_size is 0:
                    term_list.append(term)
                    freq_py_list.append([0]*len(py_options))
                    freq_py_list[0][py_index] = 1
                    dtm[d][0] = 1
                    continue
                elif term in term_list:
                    try:
                        index = term_list.index(term)
                        freq_py_list[index][py_index] += 1
                        # consider TF
                        # DTM[d][index] += 1
                        # without TF
                        dtm[d][index] = 1
                        continue
                    except Exception:
                        raise Exception("Failed to add {} to {}".format(term, file_name))
                elif term not in term_list:
                    term_list.append(term)
                    freq_py_list.append([0]*len(py_options))
                    freq_py_list[0][py_index] = 1
                    # DTM = np.c_[DTM, np.zeros([D_size,1])]
                    # np.concatenate with axis is faster
                    dtm = np.concatenate((dtm, np.zeros((documents_size,1))), axis=1)
                    dtm[d][term_size] = 1
                    continue
            else:
                continue

    with open("../data/DTM/{}.npy".format(file_name), 'wb+') as f:
        np.save(f, dtm)

    term_size = len(term_list)
    freq_size = len(freq_py_list)
    term_set_list = []
    with open("../data/term/{}.npy".format(file_name), 'wb+') as term_file:
        if term_size == freq_size:
            for j in range(term_size):
                term_vector = dtm[:, j]
                bhs = []
                bhs_index = [x for x in range(len(term_vector)) if term_vector[x] == 1]
                for index in bhs_index:
                    bhs.append(documents[index])
                freq = [str(x) for x in freq_py_list]
                term_set_list.append([term_list[j], ','.join(freq), ','.join(bhs)])
            term_set_array = np.array(term_set_list)
            # print("Shape of term array for {} is {}".format(file_name, term_set_array.shape))
            np.save(term_file, term_set_array)
        else:
            print("Error: size of frequency list is not equal to term list")

    return dtm.shape


def group_by_journal():
    journal_list = getJournals()

    for journal in journal_list:
        if journal == 'TSG' or journal == 'ZGTSGXB':
            start = time.time()
            print("Generating {} DTM ... ".format(journal), flush=False)

            triple_files = glob.glob('../data/triple/IS-{}-*.txt'.format(journal))
            print(len(triple_files))
            if len(triple_files) == 0:
                raise Exception("No matching files for {}".format(journal))

            records_merge = []
            documents_merge = []
            for i in range(len(triple_files)):
                file = txt2list.txt2list(triple_files[i])
                records = file.convert(",")
                if i == 0:
                    records_merge = records
                    documents_merge = np.unique(records[:, 0])
                else:
                    records_merge = np.concatenate((records_merge, records), axis=0)
                    documents_merge = np.concatenate((documents_merge, np.unique(records[:, 0])), axis=0)

            dtm_shape = convert(records_merge, documents_merge, journal)
            duration = float("{0:.2f}".format(time.time() - start))
            try:
                log_file.write("{}\t{}\t{}\n".format(journal, dtm_shape, duration))
                print("finished in {} sec.".format(duration), flush=True)
            except Exception:
                raise Exception("Failed to log {}".format(journal))
        else:
            pass


def group_by_py():
    triple_list = glob.glob('../data/triple/IS*.txt')
    length = len(triple_list)

    for count in range(length):
        if count < length:
            input_file = triple_list[count]
            file_name = re.search('triple(.+?).txt', input_file).group(1)[1:]
            # py = re.split(r'[-]', file_name)[-1]

            start = time.time()
            print("Generating {} DTM by year ... ".format(file_name), flush=False)

            file = txt2list.txt2list(input_file)
            records = file.convert(",")
            documents = np.unique(records[:, 0])

            dtm_shape = convert(records, documents, file_name)
            duration = float("{0:.2f}".format(time.time() - start))
            try:
                log_file.write("{}\t{}\t{}\n".format(file_name, dtm_shape, duration))
                print("finished in {} sec.".format(duration), flush=True)
            except Exception:
                raise Exception("Failed to log {}".format(file_name))

    else:
        pass

    log_file.close()


if __name__ == '__main__':
    log_file = open('../log/DTM.txt', 'a+', encoding='utf-8')
    log_file.write("File_name\tDTM_shape\tDuration\n")
    # group_by_py()
    group_by_journal()
    log_file.close()





