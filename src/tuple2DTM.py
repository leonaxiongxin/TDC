"""
  tuple2DTM.py
  convert tuple to DTM matrix
  and track the journal and py of each term
"""
import time
import txt2list
import numpy as np


def get_journals(field):
    with open('../data/journals_{}.txt'.format(field), encoding='utf-8') as f:
        line = f.readline()
        return line.split(',')


def convert():
    """
    @description: read the merged records, convert them to single DTM matrix
    @return: output DTM, term list with index, tf(in total term space), df
    """
    print("Generating {} DTM ... ".format(time_flag), flush=False)
    start_time = time.time()

    records = []
    documents = []
    journal_py_flags = []
    journal_list = []

    SUBJECTS = ['IS', 'CS', 'MS']
    for SUBJECT in SUBJECTS:
        records_new = np.load('../data/DTM/{}-records-{}.npy'.format(SUBJECT, time_flag))
        documents_new = np.load('../data/DTM/{}-documents-{}.npy'.format(SUBJECT, time_flag))
        journal_py_flags_new = np.load('../data/DTM/{}-documents-flags-{}.npy'.format(SUBJECT, time_flag))
        journals = get_journals(SUBJECT)

        records.extend(records_new)
        documents.extend(documents_new)
        journal_list.extend(journals)

        if len(journal_py_flags) == 0:
            journal_py_flags = journal_py_flags_new.tolist()
        else:
            merge_flag = journal_py_flags[-1][-1][-1]
            journal_py_flags_new = journal_py_flags_new + (merge_flag + 1)
            journal_py_flags.extend(journal_py_flags_new.tolist())

    records_size = len(records)
    documents_size = len(documents)

    journal_size = len(journal_list)
    py_size = len(py_list)
    term_list = []
    term_tf = []
    dtm = np.zeros((documents_size, 1), order="F")

    for i in range(journal_size):
        journal = journal_list[i]
        journal_term_track = []
        for j in range(py_size):
            py = py_list[j]
            journal_py_term_track = []
            start = journal_py_flags[i][j][0]
            end = journal_py_flags[i][j][1]
            print(start, end)
            for d in range(start, end + 1):
                document = documents[d]
                for r in range(records_size):
                    record = records[r]
                    bh = record[0]
                    term_size = len(term_list)
                    if bh == document:
                        term = record[-1]
                        if term_size is 0:
                            term_list.append(term)
                            term_tf.append(1)
                            dtm[d][0] = 1
                            journal_term_track.append(0)
                            journal_py_term_track.append(0)
                            continue
                        elif term in term_list:
                            try:
                                index = term_list.index(term)
                                term_tf[index] += 1
                                # consider TF
                                # dtm[d][index] += 1
                                # without TF
                                dtm[d][index] = 1
                                if index in journal_py_term_track:
                                    pass
                                else:
                                    journal_py_term_track.append(index)
                                    if index in journal_term_track:
                                        pass
                                    else:
                                        journal_term_track.append(index)
                                continue
                            except Exception:
                                raise Exception("Failed to add {} to DTM".format(term))
                        elif term not in term_list:
                            term_list.append(term)
                            term_tf.append(1)
                            # DTM = np.c_[DTM, np.zeros([D_size,1])]
                            # np.concatenate with axis is faster
                            dtm = np.concatenate((dtm, np.zeros((documents_size, 1))), axis=1)
                            dtm[d][term_size] = 1
                            journal_term_track.append(term_size)
                            journal_py_term_track.append(term_size)
                            continue
                    else:
                        continue
            term_size = len(term_list)

            with open('../data/track/{}-{}-track-{}.npy'.format(journal, time_flag, py), 'wb+') as f:
                np.save(f, np.array(journal_py_term_track))
                log_file.write("{}-{}-{}\t{}\t{}\n".format(journal, time_flag, py, len(journal_py_term_track), term_size))

        with open('../data/track/{}-{}-track.npy'.format(journal, time_flag), 'wb+') as f:
                np.save(f, np.array(journal_term_track))
                log_file.write("{}-{}\t{}\t{}\n".format(journal, time_flag, len(journal_term_track), term_size))

    with open("../data/DTM/{}-dtm-{}.npy".format(FIELD, time_flag), 'wb+') as f:
        np.save(f, dtm)

    with open("../data/term/{}-term-{}.npy".format(FIELD, time_flag), 'wb+') as term_file:
        term_df_tf = []
        if term_size == len(term_tf):
            for t in range(term_size):
                term_vector = dtm[:, t]
                bhs = term_vector[term_vector > 0]
                df = len(bhs)
                tf = term_tf[t]
                term_df_tf.append([term_list[t], df, tf])
            np.save(term_file, np.array(term_df_tf))
        else:
            print("Error: size of frequency list is not equal to term list")

    duration = float("{0:.2f}".format(time.time() - start_time))
    print("finished in {} sec.".format(duration), flush=True)
    log_file.write("{}-{}\t{}\t{}\n".format(FIELD, time_flag, term_size, duration))


def init():
    """
    @description: initialize the tuple files to merged nd array
    @return: output arrays of journal_py_flags, documents_merge, records_merge
    """
    journal_list = get_journals(FIELD)
    journal_size = len(journal_list)
    py_size = len(py_list)
    journal_py_flags = np.zeros((journal_size, py_size, 2), dtype=np.int32)

    records_merge = []
    documents_merge = []

    for i in range(journal_size):
        journal = journal_list[i]

        for j in range(py_size):
            py = py_list[j]

            # convert tuple file to list format, using txt2list class
            tuple_file = '../data/tuple/{}-{}.txt'.format(journal, py)
            file = txt2list.txt2list(tuple_file)
            records = file.convert(",")

            # merge records from all journals
            start = len(documents_merge)
            if start == 0:
                records_merge = records
                documents_merge = np.unique(records[:, 0])
            else:
                records_merge = np.concatenate((records_merge, records), axis=0)
                documents_merge = np.concatenate((documents_merge, np.unique(records[:, 0])), axis=0)
            end = len(documents_merge)
            journal_py_flags[i, j, :] = [start, end - 1]

    # [journal_size, py_size, 2]
    # For each journal at each PY, tag the start and end index of documents_marge.
    with open('../data/DTM/{}-documents-flags-{}.npy'.format(FIELD, time_flag), 'wb+') as f:
        np.save(f, journal_py_flags)

    # documents_marge, list of unique document_id
    with open('../data/DTM/{}-documents-{}.npy'.format(FIELD, time_flag), 'wb+') as f:
        np.save(f, documents_merge)

    # records_marge, list of records
    with open('../data/DTM/{}-records-{}.npy'.format(FIELD, time_flag), 'wb+') as f:
        np.save(f, records_merge)


if __name__ == '__main__':
    # FIELDS = ['IS', 'CS', 'MS']
    # FIELDS = ['CS', 'MS']
    FIELDS = ['IS-CS-MS']
    # Default time range to [2013, 2017]
    PYS = 1
    py_list = []
    time_flag = ''
    for FIELD in FIELDS:
        log_file = open('../log/{}-DTM-log.txt'.format(FIELD), 'a+', encoding='utf-8')
        log_file.write("Type\tLength of term\tduration\n")

        if PYS == 1:
            py_list = [2017]
            time_flag = '17'
        elif PYS == 5:
            py_list = np.arange(2013, 2018, 1)
            time_flag = '13-17'
        # init()
        convert()

        log_file.close()
