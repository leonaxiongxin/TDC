import numpy as np
import matplotlib.pyplot as plt


def getJournals():
    journals_list = []
    with open('../data/journals_zh.txt', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            journals_list.append(line.strip())
    journals = np.array(journals_list)
    with open('../data/journals_zh.npy', 'wb+') as f:
        np.save(f, np.array(journals))


# comparision between journals
# 1 line
def group_by_journal():
    x = np.load('../data/journals_zh.npy')
    tdc = np.load("../data/tdc_by_journal.npy")
    plt.figure(figsize=(8, 5))
    plt.xlabel("Journal")
    plt.ylabel("TDC")
    plt.xticks(rotation=45)
    plt.plot(x, tdc, marker='o')
    plt.show()


# comparision between publication years
# 18 lines
def group_by_py():
    journals = np.load('../data/journals_zh.npy')
    tdc = np.load("../data/tdc_by_py.npy")
    plt.figure(figsize=(3, 10))
    pys = np.arange(2013., 2018.)
    size = len(journals)

    for i in range(size):
        start = i * 5
        ax = plt.subplot(6, 3, i + 1)
        ax.set_title(journals[i])
        # plt.plot(pys, tdc[start:start+5], marker='o', label=journals[i], linewidth=2.0)
        plt.plot(pys, tdc[start:start+5], marker='o', linewidth=2.0)
        plt.ylabel("TDC")
        # 设置坐标轴范围
        plt.xlim((2013, 2017))
        plt.ylim((-0.006, 0.012))
        # 设置坐标轴刻度
        x_ticks = np.arange(2013, 2018)
        y_ticks = np.arange(-0.006, 0.012, 0.006)
        plt.xticks(x_ticks)
        plt.yticks(y_ticks)
        # 调整子图之间的距离
        plt.tight_layout()
    # plt.axis([2013., 2017.,  -0.006, 0.012])
    # plt.legend(loc='upper right')
    # plt.grid()
    plt.show()

if __name__ == '__main__':
    # Matplotlib中设置字体-黑体，解决Matplotlib中文乱码问题
    plt.rcParams['font.sans-serif']=['SimHei']
    # 解决Matplotlib坐标轴负号'-'显示为方块的问题
    plt.rcParams['axes.unicode_minus'] = False
    # getJournals()
    # group_by_journal()
    group_by_py()
    exit(-1)
