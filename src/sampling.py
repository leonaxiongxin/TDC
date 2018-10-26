import random
import numpy as np


def remainOrigin(dataSet):
    return dataSet


def randomSampling(dataSet, scale):
    """简单随机抽样

    """
    try:
        # random.sample()保持原来的顺序
        data_sample = random.sample(dataSet, scale)
        data_sample.sort()
        return np.array(data_sample)
    except Exception as e:
        print("random sampling: {}".format(e))
        return None


def repetitionRandomSampling(dataSet, scale):
    """重复随机抽样

    """
    data_sample = []
    try:
        for i in range(scale):
            data_sample.append(dataSet[random.randint(0, len(dataSet) - 1)])
        return np.array(data_sample)
    except Exception as e:
        print(e)
        return None


def systematicSampling(dataSet, scale):
    """系统抽样，等距抽样

    """
    data_sample = []
    length = len(dataSet)
    distance = int(length / scale)
    count = 0
    try:
        if distance > 0:
            while len(data_sample) < scale:
                data_sample.append(dataSet[count * distance])
                count += 1
            return data_sample
        else:
            return randomSampling(dataSet, scale)
    except Exception as e:
        print(e)
        return None


def stratifiedSampling(dataSet, sampling_label, label_index, sampling_index, sampling_type, scale):
    """分层抽取样本

    Args:
        sampling_label: 分层抽样的标签/索引
        sampling_index: 分层抽样的标签在数据样本中的列索引
        sampling_type: 随机类型，仅支持 ro, rs，rrs，ss，分别是不抽样，随机抽样，重复随机抽样，系统抽样
        scale：抽取样本个数，值域为 (0, 样本的总数)

    """
    data_sample = []
    length = len(dataSet)
    size = int(scale/len(sampling_label))

    for label in sampling_label:
        data_labeled = []
        for j in range(length):
            # type(value) = string
            labeled_value = dataSet[j][label_index]
            if labeled_value == label:
                data_labeled.append(dataSet[j][sampling_index])
            else:
                pass

        if len(data_labeled) > 0:
            if sampling_type == 'rs':
                sampling_result = randomSampling(data_labeled, size)
                data_sample.append(sampling_result)
            elif sampling_type == 'rrs':
                sampling_result = repetitionRandomSampling(data_labeled, size)
                data_sample.append(sampling_result)
            elif sampling_type == 'ss':
                sampling_result = systematicSampling(data_labeled, size)
                data_sample.append(sampling_result)
            elif sampling_type == 'ro':
                sampling_result = remainOrigin(data_labeled)
                data_sample.append(sampling_result)
            else:
                raise Exception('unsupported sampling type: {}'.format(sampling_type))
        else:
            print('Length of {} labeled data is: {}'.format(label, len(data_labeled)))

    return np.array(data_sample)




