"""
  track2txt.py
  convert npy file of tdc values to txt file
  according to the index tracking of each journal
  and draw the box figure
"""
import numpy as np
import matplotlib.pyplot as plt


def get_journals(field):
    with open('../data/journals_{}.txt'.format(field), encoding='utf-8') as f:
        line = f.readline()
        return line.split(',')


def group_by_journal_box(data, labels):
    """
    @description: box plot for each journal
    @param data: nd array
    @param labels: 1d array
    @return: 1 box plot
    """
    # top = 5
    # bottom = -2
    top = 3
    bottom = -1
    y_step = 1
    plt.figure(figsize=(14, 5))
    plt.ylabel("TDC", font)
    plt.boxplot(data, sym="o", whis=1.5, labels=labels)
    plt.tick_params(colors='black', width=2, labelsize=18, labelcolor='black')
    # plt.tick_params(axis='x', )
    # plt.tick_params(axis='y', colors='black', linewidth=0.25)
    y_ticks = np.arange(bottom, top + 1, y_step)
    plt.yticks(y_ticks)
    plt.show()


def group_by_journal_hist(data, labels):
    """
    @description: hist plot for each journal
    @param data: nd array
    @param labels: 1d array
    @return: multiple hist plot
    """
    upper = 5
    bottom = -3
    x_step = 1
    y_step = 0.2
    intervals = np.arange(bottom, upper + 1, 1)
    size = len(labels)
    categories = len(intervals)

    plt.figure(figsize=(10, 8))

    for i in range(size):
        tdc = data[i]
        ax = plt.subplot(3, 6, i + 1)
        ax.set_title(labels[i])
        plt.hist(tdc, bins=categories, range=[bottom, upper], density=1, histtype='bar', align="left", alpha=0.75)
        # n, bins_limits, patches = plt.hist(tdc, bins=categories, range=[bottom, upper], density=1, histtype='bar', align="left", alpha=0.75)
        # plt.plot(bins_limits[:categories], n, '-')
        plt.xlabel("TDC value")
        plt.ylabel("Frequency %")
        # 设置坐标轴范围
        plt.xlim((bottom, upper - x_step))
        plt.ylim((0, 1))
        # 设置坐标轴刻度
        x_ticks = np.arange(bottom, upper - x_step)
        y_ticks = np.arange(0, 1, y_step)
        plt.xticks(x_ticks)
        plt.yticks(y_ticks)
        plt.tight_layout()
    plt.show()


def track():
    tdc_all = np.load("../data/TDC/{}-tdc-{}.npy".format(FIELD, time_flag))
    term_all = np.load("../data/term/{}-term-{}.npy".format(FIELD, time_flag))

    journal_size = len(journal_list)

    # for individual journal
    with open("../data/term/{}-tdc-journal-test-{}.txt".format(FIELD, time_flag), "a+", encoding="gbk") as journal_term_file:
        journal_term_file.write('journal, tdc, df, tf, term\n')

        tdc_journal_list = []

        for j in range(journal_size):
            journal = journal_list[j]
            if j in range(0, 18):
                subject = 0
            elif j in range(18, 36):
                subject = 1
            elif j in range(36, 54):
                subject = 2

            track_file = '../data/track/{}-{}-track.npy'.format(journal, time_flag)
            track_index = np.load(track_file)
            term_size = len(track_index)

            tdc_journal = np.zeros(term_size, dtype=np.float32)

            for count in range(term_size):
                index = track_index[count]
                tdc = tdc_all[index]
                tdc_journal[count] = tdc
                term = term_all[index][0]
                df = term_all[index][1]
                tf = term_all[index][2]
                journal_term_file.write('{},{},{:.7f},{},{},{}\n'.format(subject, j, tdc, df, tf, term))

            # with open('../data/tdc/{}-tdc-journal-{}.npy'.format(journal, time_flag), 'wb+') as tdc_journal_npy:
            #     np.save(tdc_journal_npy, tdc_journal)
            # with open('../data/tdc/{}-tdc-journal-{}.txt'.format(journal, time_flag), 'w+') as tdc_journal_txt:
            #     np.savetxt(tdc_journal_txt, tdc_journal, fmt="%.7f", delimiter=',', newline='\n')
            tdc_journal_list.append(tdc_journal.tolist())
        group_by_journal_box(tdc_journal_list, range(1, journal_size + 1))
        # group_by_journal_hist(tdc_journal_list, range(journal_size))

    # for individual journal in specific year
    # with open("../data/term/{}-tdc-py-{}.txt".format(FIELD, time_flag), "a+", encoding="gbk") as journal_py_term_file:
    #     journal_py_term_file.write('journal, tdc, py, df, tf, term\n')
    #
    #     for j in range(journal_size):
    #         journal = journal_list[j]
    #         for py in py_list:
    #             py_track_file = '../data/track/{}-{}-track-{}.npy'.format(journal, time_flag, py)
    #             track_index = np.load(py_track_file)
    #             term_size = len(track_index)
    #
    #             tdc_journal_py = np.zeros(term_size, dtype=np.float32)
    #
    #             for count in range(term_size):
    #                 index = track_index[count]
    #                 tdc = tdc_all[index]
    #                 tdc_journal_py[count] = tdc
    #                 term = term_all[index][0]
    #                 df = term_all[index][1]
    #                 tf = term_all[index][2]
    #                 journal_py_term_file.write('{},{:.7f},{},{},{},{}\n'.format(j, tdc, py, df, tf, term))


if __name__ == '__main__':
    FIELDS = ['IS']
    # FIELDS = ['IS-CS-MS']
    PYS = 1
    py_list = []
    time_flag = ''

    font = {
        'family': 'Arial',
        'weight': 'bold',
        'size': 18  # or 14
    }
    # plt.rcParams["figure.edgecolor"] = 'black'
    # plt.rcParams['axes.edgecolor'] = 'black'
    # plt.rcParams['lines.color'] = 'black'
    # plt.rcParams['axes.linewidth'] = 0.25
    # plt.rcParams['lines.linewidth'] = 0.25

    # SUBJECTS = ['IS', 'CS', 'MS']
    SUBJECTS = ['IS']
    journal_list = []
    for SUBJECT in SUBJECTS:
        journals = get_journals(SUBJECT)
        journal_list.extend(journals)

    for FIELD in FIELDS:
        if PYS == 1:
            py_list = np.arange(2017, 2018, 1)
            time_flag = '17'
        elif PYS == 5:
            py_list = np.arange(2013, 2018, 1)
            time_flag = '13-17'

        track()
