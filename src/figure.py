import numpy as np
import matplotlib.pyplot as plt


def get_journals():
    with open('../data/journals_{}.txt'.format(FIELD), encoding='utf-8') as f:
        line = f.readline()
        journals_name = line.split(',')
        journals_path = []
        for journal in journals_name:
            journals_path.append("../data/TDC/{}.npy".format(journal))
        return journals_path


def get_journals_zh():
    journals_list = []
    with open('../data/journals_{}_zh.txt'.format(FIELD), encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            journals_list.append(line.strip())
    journals = np.array(journals_list)
    with open('../data/journals_{}_zh.npy'.format(FIELD), 'wb+') as f:
        np.save(f, np.array(journals))


def group_by_journal_line():
    """
    @description: compare average tdc between journals
    @return:  1 line
    """
    bottom = 0.86
    upper = 0.98
    step = 0.02
    x = np.load('../data/journals_{}_zh.npy'.format(FIELD))
    tdc = np.load("../log/{}-tdc-by-journal.npy".format(FIELD))
    plt.figure(figsize=(16, 4))
    plt.xlabel("Journal")
    plt.ylabel("TDC")
    # 设置坐标轴范围
    plt.ylim((bottom, upper))
    # 设置坐标轴刻度
    y_ticks = np.arange(bottom - step, upper + step, step)
    plt.yticks(y_ticks)
    plt.xticks(rotation=45)
    plt.plot(x, tdc, marker='o')
    plt.show()


def group_by_journal_scatters():
    """
    @description: scatter all tdc value for each journal
    @return: multiple scatter subplots
    """
    journals = np.load('../data/journals_{}_zh.npy'.format(FIELD))
    journals_tdc_path = get_journals()
    plt.figure(figsize=(12, 5))
    size = len(journals)

    for i in range(size):
        tdc_file = journals_tdc_path[i]
        tdc = np.load(tdc_file)
        length = len(tdc)
        x = np.arange(0, length, 1)
        ax = plt.subplot(3, 6, i + 1)
        ax.set_title(journals[i])
        plt.plot(x, tdc, marker='.')
        plt.ylabel("TDC")
        # 调整子图之间的距离
        plt.tight_layout()
    plt.show()


def group_by_journal_box():
    """
    @description: box plot for each journal
    @return: 1 box plot
    """
    journals = np.load('../data/journals_{}_zh.npy'.format(FIELD))
    journals_tdc_path = get_journals()
    size = len(journals)
    tdc_lists = []
    for i in range(size):
        tdc = np.load(journals_tdc_path[i])
        tdc_lists.append(tdc)
    print(len(tdc_lists), len(journals))
    plt.figure(figsize=(8, 5))
    plt.ylabel("TDC")
    plt.xticks(rotation=45)
    plt.boxplot(tdc_lists, labels=journals)
    plt.show()


def group_by_journal_hist():
    """
    @description: box plot for each journal
    @return: 1 box plot
    """
    upper = 6
    bottom = -2
    intervals = np.arange(bottom, upper + 1, 1)
    journals = np.load('../data/journals_{}_zh.npy'.format(FIELD))
    journals_tdc_path = get_journals()
    size = len(journals)
    categories = len(intervals)

    plt.figure(figsize=(12, 5))

    for i in range(size):
        tdc = np.load(journals_tdc_path[i])
        # total = len(tdc)
        # count = np.zeros(categories)
        # for j in range(categories - 1):
        #     mark = intervals[j+1]
        #     target = tdc[tdc < mark]
        #     target_count = len(target) - np.sum(count)
        #     count[j] = target_count
        # frequency = count / total
        ax = plt.subplot(3, 6, i + 1)
        ax.set_title(journals[i])
        # plt.bar(intervals, frequency, tick_label=intervals)
        plt.hist(tdc, bins=categories, range=[bottom, upper], density=1, histtype='bar', align="left", alpha=0.75)
        # n, bins_limits, patches = plt.hist(tdc, bins=categories, range=[bottom, upper], density=1, histtype='bar', align="left", alpha=0.75)
        # plt.plot(bins_limits[:categories], n, '-')
        plt.xlabel("TDC value")
        plt.ylabel("Frequency %")
        # 设置坐标轴范围
        plt.xlim((bottom - 2, upper - 1))
        plt.ylim((0, 1))
        # 设置坐标轴刻度
        x_ticks = np.arange(bottom - 2, upper - 1)
        y_ticks = np.arange(0, 1, 0.2)
        plt.xticks(x_ticks)
        plt.yticks(y_ticks)
        plt.tight_layout()
    plt.show()


def group_by_py_line():
    """
    @description: compare tdc between publication years for each journal
    @return: multiple subplots
    """
    bottom = 0.93
    upper = 1.00
    step = 0.02
    journals = np.load('../data/journals_{}_zh.npy'.format(FIELD))
    tdc = np.load("../log/{}-tdc-by-py.npy".format(FIELD))
    pys = np.arange(2013., 2018.)
    size = len(journals)

    plt.figure(figsize=(12, 5))

    for i in range(size):
        start = i * 5
        ax = plt.subplot(3, 6, i + 1)
        ax.set_title(journals[i])
        # plt.plot(pys, tdc[start:start+5], marker='o', label=journals[i], linewidth=2.0)
        plt.plot(pys, tdc[start:start+5], marker='o', linewidth=2.0)
        plt.ylabel("TDC")
        # 设置坐标轴范围
        plt.xlim((2013, 2017))
        plt.ylim((bottom, upper))
        # 设置坐标轴刻度
        x_ticks = np.arange(2013, 2018)
        y_ticks = np.arange(bottom - step, upper + step, step)
        plt.xticks(x_ticks)
        plt.yticks(y_ticks)
        # 调整子图之间的距离
        plt.tight_layout()
    # plt.axis([2013., 2017.,  -0.006, 0.012])
    # plt.legend(loc='upper right')
    # plt.grid()
    plt.show()


def group_by_py_lines():
    """
    @description: compare tdc between publication years for each journal
    @return: multiple subplots
    """
    bottom = 0.93
    upper = 1.00
    step = 0.02
    journals = np.load('../data/journals_{}_zh.npy'.format(FIELD))
    tdc = np.load("../log/{}-tdc-by-py.npy".format(FIELD))
    pys = np.arange(2013., 2018.)
    size = len(journals)

    plt.figure(figsize=(12, 5))

    for i in range(size):
        start = i * 5
        plt.plot(pys, tdc[start:start+5], marker='o', label=journals[i], linewidth=2.0)
        plt.ylabel("TDC")
    # 设置坐标轴范围
    plt.xlim((2013, 2017))
    plt.ylim((bottom, upper))
    # 设置坐标轴刻度
    x_ticks = np.arange(2013, 2018)
    y_ticks = np.arange(bottom - step, upper + step, step)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    # plt.axis([2013., 2017.,  -0.006, 0.012])
    plt.legend(loc='upper right')
    # plt.grid()
    plt.show()


def group_by_field_line():
    """
    @description: compare average tdc between journals
    @return:  1 line
    """
    plt.figure(figsize=(16, 4))
    bottom = 0.86
    upper = 0.98
    step = 0.02
    fields = ['IS', 'PHY', 'CS']
    for field in fields:
        x = np.load('../data/journals_{}_zh.npy'.format(field))
        tdc = np.load("../log/{}-tdc-by-journal.npy".format(field))
        plt.plot(x, tdc, marker='o')
    plt.xlabel("Journal")
    plt.ylabel("TDC")
    # 设置坐标轴范围
    plt.ylim((bottom, upper))
    # 设置坐标轴刻度
    y_ticks = np.arange(bottom - step, upper + step, step)
    plt.yticks(y_ticks)
    plt.xticks(rotation=45)
    plt.show()


if __name__ == '__main__':
    # 设置字体为黑体，解决中文乱码问题
    plt.rcParams['font.sans-serif']=['SimHei']
    # 解决坐标轴负号'-'显示为方块的问题
    plt.rcParams['axes.unicode_minus'] = False

    # FIELD = ['IS','CS','PHY']
    FIELD = 'PHY'

    # get_journals_zh()
    # group_by_journal_line()
    # group_by_journal_scatters()
    # group_by_journal_box()
    # group_by_journal_hist()

    group_by_py_line()
    # group_by_py_lines()
    # group_by_field_line()
    exit(-1)
