"""
  xml2tuple.py
  convert xml to tuple set
"""

import glob
import time
import re
import xml2csv
import txt2list
# from pynlpir import nlpir
import pynlpir
from ctypes import c_char_p
import sampling
import numpy as np


def xml2txt():
    start = time.time()
    print("Generating csv ... ", flush=True)

    journal_list = glob.glob("../data/xml/{}*.xml_DR.xml".format(FIELD))

    length = len(journal_list)

    tag = "Bibliography"
    ignore_list = ['DT', 'AD', 'TIss', 'SO', 'IS', 'ABss', 'SP', 'EP', 'LA', 'AUs', 'AUf']

    for count in range(length):
        if count < length:
            input_file = journal_list[count]
            journal_name = re.search('{}-(.+?).xml_DR.xml'.format(FIELD), input_file).group(1)
            output_file = "../data/csv/{}-{}.csv".format(FIELD, journal_name)
            print(input_file, output_file, "\n")
            file = xml2csv.xml2csv(input_file, output_file)
            file.convert(tag, ignore_list, "\t")
        else:
            pass

    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)


def write_tuple(bh, py, ss, source, foutput, file_name):
    removeSpeech = [
        'particle',
        'punctuation mark',
        'conjunction',
        'preposition',
        # 'adverb',
        'noun of locality',
        'pronoun',
        'modal particle',
        'onomatopoeia',
        'string',
        'suffix',
        'interjection',
        'numeral',
        'prefix',
        'classifier',
        'status word'
    ]

    # use classical stop words list instead
    # removeSpeech = [
    #     'punctuation mark',
    # ]
    stopWords = np.load('ChineseStopWords.npy')
    stopWordsList = stopWords.tolist()

    for wordPair in ss:
        word = wordPair[0]
        speech = wordPair[1]
        if word == ' ':
            continue
        elif speech is None:
            print("{} is not recognized by NLPIR".format(word))
            log_file.write(file_name + str(bh) + word + '\n')
        elif speech in removeSpeech:
            continue
        elif word in stopWordsList:
            continue
        else:
            foutput.write('{}-{},{},{},{},{}\n'.format(file_name, bh, py, source, speech, word))


def txt2tuple():
    csv_list = glob.glob("../data/csv/{}*.csv".format(FIELD))
    length = len(csv_list)

    if length == 0:
        raise Exception("No matching file!")

    for count in range(length):
        input_file = csv_list[count]
        # file_name = re.search('{}(.+?)-13-17.csv'.format(FIELD), input_file).group(1)[1:]
        file_name = re.search('{}(.+?).csv'.format(FIELD), input_file).group(1)[1:]

        start = time.time()
        print("Generating {} tuple ... ".format(file_name), flush=True)

        file = txt2list.txt2list(input_file)
        records = file.convert("\t")
        rows = records.shape[0]

        # with sampling, 40 records per year
        # optional operation
        if count < length:
            print(count)
            sampling_data = []
            sampling_labels = np.arange(2013, 2018)
            for i in range(rows):
                record = records[i]
                bh = i
                py = int(record[1])
                sampling_data.append([bh, py])
            sampling_input = np.array(sampling_data)
            sampling_index = 0
            label_index = 1
            # 每年的采样数应该一致
            sampling_type = 'rs'
            scale = 40 * len(sampling_labels)
            sampling_output = sampling.stratifiedSampling(sampling_input,
                                                          sampling_labels,
                                                          label_index,
                                                          sampling_index,
                                                          sampling_type,
                                                          scale
                                                          )
            # print("Length of sampling data is: {}\nShape of sampling result is: {}".format(len(sampling_data), sampling_output.shape))
            for j in range(len(sampling_labels)):
                result = sampling_output[j]
                py = sampling_labels[j]

                output_file = open("../data/tuple/{}-{}-{}.txt".format(FIELD, file_name, str(py)), 'w+', encoding='utf-8')
                output_file.write('bh,py,src,speech,word\n')

                for bh in result:
                    record = records[bh]
                    TIss = pynlpir.segment(record[0])
                    # do not segment keywords
                    # KWs = re.split(r'[|]',record[2])[:-1]
                    # segment keywords
                    KWs = pynlpir.segment(record[2])
                    AB = re.split(r'[<正>]', record[3])[-1]
                    ABss = pynlpir.segment(AB)
                    write_tuple(bh, py, TIss, 4, output_file, file_name)
                    write_tuple(bh, py, KWs, 2, output_file, file_name)
                    write_tuple(bh, py, ABss, 1, output_file, file_name)
                output_file.close()

            print("finished in {:.2f} sec.".format(time.time() - start), flush=True)

        # without sampling, full records
        elif count > length:
            output_file = open("../data/tuple/Full/{}-{}.txt".format(FIELD, file_name), 'w+', encoding='utf-8')
            output_file.write('bh,py,src,speech,word' + '\n')

            for i in range(rows):
                record = records[i]
                bh = i
                TIss = pynlpir.segment(record[0])
                py = record[1]
                # KWs = re.split(r'[|]',record[2])[:-1]
                KWs = pynlpir.segment(record[2])
                AB = re.split(r'<[正]>', record[3])[-1]
                ABss = pynlpir.segment(AB)
                write_tuple(bh, py, TIss, 4, output_file)
                write_tuple(bh, py, KWs, 2, output_file)
                write_tuple(bh, py, ABss, 1, output_file)

            output_file.close()
            print("finished in {:.2f} sec.".format(time.time() - start), flush=True)
        else:
            pass


if __name__ == '__main__':
    # FIELDS = ['IS', 'CS', 'MS']
    FIELDS = ['CS', 'MS']
    for FIELD in FIELDS:
        xml2txt()
        pynlpir.open()
        # AddUserWord 加入用户词典的词不可分割
        pynlpir.nlpir.AddUserWord(c_char_p('云计算'.encode('utf-8')))
        pynlpir.nlpir.AddUserWord(c_char_p('微博'.encode('utf-8')))
        pynlpir.nlpir.AddUserWord(c_char_p('h指数'.encode('utf-8')))
        pynlpir.nlpir.AddUserWord(c_char_p('元数据'.encode('utf-8')))
        log_file = open('../log/{}-tuple-log.txt'.format(FIELD), 'a+', encoding='utf-8')
        txt2tuple()
        pynlpir.close()
        log_file.close()
