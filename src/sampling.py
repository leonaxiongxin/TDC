import random
import numpy as np


def randomSampling(dataSet, scale):
    """简单随机抽样

    """
    try:
        data_sample = random.sample(dataSet, scale)
        return np.array(data_sample)
    except Exception as e:
        print(e)
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


def stratifiedSampling(dataSet, sampling_label, sampling_index, sampling_type, scale):
    """分层抽取样本

    Args:
        sampling_label: 分层抽样的标签/索引
        sampling_index: 分层抽样的标签在数据样本中的列索引
        sampling_type: 随机类型，仅支持 rs，rrs，ss，分别是随机抽样，重复随机抽样，系统抽样
        scale：抽取样本个数，值域为 (0, 样本的总数)

    """
    data_sample = []
    length = len(dataSet)
    size = len(sampling_label)

    for label in sampling_label:
        data_labeled = []
        for j in range(length):
            value = int(dataSet[j][sampling_index])
            if value == label:
                data_labeled.append(dataSet[j])
            else:
                pass
        print('Length of {} labeled data is: {}'.format(label, len(data_labeled)))

        if len(data_labeled) > 0:
            if sampling_type == 'rs':
                sampling_result = randomSampling(data_labeled, scale / size)
                data_sample.append(sampling_result)
            elif sampling_type == 'rrs':
                sampling_result = repetitionRandomSampling(data_labeled, scale / size)
                data_sample.append(sampling_result)
            elif sampling_type == 'ss':
                sampling_result = systematicSampling(data_labeled, scale / size)
                data_sample.append(sampling_result)
            else:
                raise Exception('unsupported sampling type: {}'.format(sampling_type))
        else:
             raise Exception('{} label data went wrong'.format(label))

    return np.array(data_sample)




