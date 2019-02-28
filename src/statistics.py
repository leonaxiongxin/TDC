import numpy as np
import re
from scipy import stats
import math


class StatisticalAnalyze:
    def __init__(self, input_file, output_file, encoding='utf-8'):
        """
        Initialize the class with the paths to the input npy file and the output csv file
        @params input_file ：input xml filename
        @params output_file: output csv filename
        @params encoding: character encoding
        """

        # open the xml file for iteration
        self.data = np.load(input_file)

        # output file handle
        try:
            with open(output_file, 'w+', encoding=encoding) as output:
                np.savetxt(output_file, self.data, fmt='%.7f', delimiter=',', newline='\n')
        except Exception:
            print("Failed to open the {}".format(output_file))
            raise

    def descriptive_statistics(self):
        nobs, min_max, mean, var, skewness, kurt = stats.describe(self.data)
        std = math.sqrt(var)

        return {'nobs': nobs, 'mean': mean, 'min': min_max[0], 'max': min_max[1],
                'std': std, 'skewness': skewness, 'kurt': kurt}

    def frequency_count(self):
        positive = self.data[self.data > 0]
        total_count = len(self.data)
        positive_count = len(positive)
        positive_percent = positive_count / total_count
        return positive_count, positive_percent


def get_journals_path():
    with open('../data/journals_{}.txt'.format(FIELD), encoding='utf-8') as f:
        line = f.readline()
        journals_name = line.split(',')
        journals_path = []
        for journal in journals_name:
            journals_path.append("../data/TDC/{}.npy".format(journal))
        return journals_path


def confident_interval(mean, std):
        # 求正态分布95%置信区间
        ci = stats.norm.interval(0.95, loc=mean, scale=std)
        return {'bottom': ci[0], 'upper': ci[1]}


def statistics(tdc_journals_list):
    """
    @param tdc_journals_list: files of tdc
    @return: descriptive analysis of tdc for each journal
    """
    length = len(tdc_journals_list)

    log_file = open('../analysis/{}-TDC-Descriptive.txt'.format(FIELD), 'a+', encoding='utf-8')
    log_file.write('期刊\t计数\t均值\t极小值\t极大值\t标准差\t正值个数\t正值百分比\t偏度\t峰度\t95%置信区间下限\t95%置信区间上限\n')

    for i in range(length):
        if i < length:
            input_file = tdc_journals_list[i]
            file_name = re.search('{}-(.+?).npy'.format(FIELD), input_file).group(1)
            output_file = '../data/tdc/{}-{}.csv'.format(FIELD, file_name)

            sa = StatisticalAnalyze(input_file, output_file)
            ds = sa.descriptive_statistics()
            nobs = ds['nobs']
            mean = ds['mean']
            minimum = ds['min']
            maximum = ds['max']
            std = ds['std']
            skewness = ds['skewness']
            kurt = ds['kurt']
            ci = confident_interval(mean, std)
            bottom = ci['bottom']
            upper = ci['upper']
            positive_count, positive_percent = sa.frequency_count()

            log_file.write('{}\t{}\t{:.7f}\t{:.7f}\t{:.7f}\t{:.7f}\t{}\t{:.4f}\t{:.7f}\t{:.7f}\t{:.7f}\t{:.7f}\n'.format(
                file_name, nobs, mean, minimum, maximum, std, positive_count, positive_percent, skewness, kurt, bottom, upper)
            )
        else:
            pass

    log_file.close()


def gradient():
    journals = np.load('../data/journals_{}_zh.npy'.format(FIELD))
    pys = np.arange(2013, 2018, 1)
    tdc_by_py = np.load("../log/{}-tdc-by-py.npy".format(FIELD))
    size_journals = len(journals)
    size_pys = len(pys)
    tdc_reshape = tdc_by_py.reshape([size_journals, size_pys])
    gradients = np.zeros((size_journals, size_pys), dtype=np.float32)
    for i in range(size_journals):
        tdc = tdc_reshape[i, :]
        gradients[i, :] = np.array(np.gradient(tdc))

    with open('../analysis/{}-TDC-Gradient.txt'.format(FIELD), 'w+', encoding='utf-8') as f:
        for i in range(size_journals):
            for j in range(size_pys):
                f.write('{:7f}\t'.format(gradients[i, j]))
            f.write('\n')

    with open('../analysis/{}-TDC-by-py.txt'.format(FIELD), 'w+', encoding='utf-8') as f:
        for i in range(size_journals):
            for j in range(size_pys):
                f.write('{:7f}\t'.format(tdc_reshape[i, j]))
            f.write('\n')


if __name__ == '__main__':
    FIELDS = ['IS', 'CS', 'PHY']
    # FIELDS = ['IS']
    for FIELD in FIELDS:
        tdc_journals_path = get_journals_path()
        # statistics(tdc_journals_path)
        gradient()
