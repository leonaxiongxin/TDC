"""
  xml2triple.py
  convert xml to triple set
"""

import glob
import time
import re
import xml2csv
import txt2list
# from pynlpir import nlpir
import pynlpir
from ctypes import c_char_p
import numpy as np
import sampling


def xml2txt():
    start = time.time()
    print("Generating csv ... ", flush=True)

    # for IS journal
    journal_list = glob.glob("../xmldata/IS*.xml_DR.xml")

    # for PHY journal
    # journal_list = glob.glob("../xmldata/PHY*.xml_DR.xml")

    tag = "Bibliography"
    ignore_list = ['DT', 'AD', 'TIss', 'SO', 'IS', 'ABss', 'SP', 'EP', 'LA', 'AUs', 'AUf']

    for journal in journal_list:
        input_file = journal
        journal_name = re.search('xmldata(.+?).xml_DR.xml', journal).group(1)
        output_file = "../csvFull{}.csv".format(journal_name)
        print(input_file, output_file, "\n")
        file = xml2csv.xml2csv(input_file, output_file)
        file.convert(tag, ignore_list, "\t")

    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)


def kws2userdict():
    start = time.time()
    print("Generating user dict ... ", flush=True)

    csv_list = glob.glob("../csvFull/*.csv")

    fdict = open("../IS-userdict.txt", "w+", encoding="utf-8")

    userdict = []

    for csv in csv_list:
        input_file = csv
        file = txt2list.txt2list(input_file)
        lists = file.convert("\t")
        rows = lists.shape[0]
        for i in range(rows):
            record = lists[i]
            kws = re.split(r'[|]', record[2])[:-1]
            for kw in kws:
                if kw not in userdict:
                    userdict.append(kw)

    for word in userdict:
        if len(word) > 0:
            if not pynlpir.nlpir.AddUserWord(c_char_p(str(word).encode('utf-8'))):
                print('AddUserWord failed!')
                exit(-111)
            else:
                fdict.write(str(word) + '\n')

    fdict.close()
    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)


def writeTriple(bh, py, ss, source, foutput):
    removeSpeech = [
        'particle',
        'punctuation mark',
        'conjunction',
        'preposition',
        'adverb',
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
    for wordPair in ss:
        word = wordPair[0]
        speech = wordPair[1]
        if speech in removeSpeech or speech is None:
            continue
        else:
            foutput.write('{}, {}, {}, {}, {} \n'.format(bh, py, source, speech, word))


def txt2triple():
    start = time.time()
    print("Generating triple ... ", flush=True)

    # for IS journal
    csv_list = glob.glob("../csvFull/IS*.csv")

    for csv in csv_list:
        input_file = csv
        file_name = re.search('csvFull(.+?).csv', csv).group(1)[1:]

        file_output = open("../triple/{}.txt".format(file_name), 'w+', encoding='utf-8')
        file_output.write('bh,py,src,speech,word' + '\n')

        file = txt2list.txt2list(input_file)
        records = file.convert("\t")
        rows = records.shape[0]

        for i in range(rows):
            record = records[i]
            bh = i
            TIss = pynlpir.segment(record[0])
            py = record[1]
            # KWs = re.split(r'[|]',record[2])[:-1]
            KWs = pynlpir.segment(record[2])
            AB = re.split(r'[<正>]', record[3])[-1]
            ABss = pynlpir.segment(AB)
            writeTriple(bh, py, TIss, 0, file_output)
            writeTriple(bh, py, KWs, 1, file_output)
            writeTriple(bh, py, ABss, 2, file_output)

        file_output.close()
    print("finished in {:.2f} sec.".format(time.time() - start), flush=True)


if __name__ == '__main__':
    # xml2txt()
    pynlpir.open()
    pynlpir.nlpir.AddUserWord(c_char_p('云计算'.encode('utf-8')))
    # kws2userdict()
    txt2triple()
    pynlpir.close()
