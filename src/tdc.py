"""
  tdc.py
  Convert Document-Term Matrix to Term-Term matrix
  Compute the TDC of each term
  Compute the average value
  Via cosine similarity
"""

import glob
import time
import re
import numpy as np
from scipy.spatial.distance import pdist, squareform


def compute(ttm, size):
    centroid = np.mean(ttm, axis=0)
    dist = np.zeros(size, dtype=np.float32)
    for i in range(size):
        dist[i] = np.dot(ttm[i, :], centroid)/(np.linalg.norm(ttm[i, :])*(np.linalg.norm(centroid)))
    density = np.mean(dist)

    dist_t = np.zeros(size - 1, dtype=np.float32)
    density_t = np.zeros(size, dtype=np.float32)
    for i in range(size):
        ttm_c = np.delete(ttm, i, axis=0)
        ttm_t = np.delete(ttm_c, i, axis=1)
        centroid_i = np.mean(ttm_t, axis=0)
        for j in range(size - 1):
            dist_t[j] = np.dot(ttm_t[j, :], centroid_i)/(np.linalg.norm(ttm_t[j, :])*(np.linalg.norm(centroid_i)))

        density_t[i] = np.mean(dist_t)

    density_avg = np.sum(np.fabs(density_t - density)) / size
    tdc = (density_t - density) / density_avg

    return density_avg, tdc


def main(dtm_list, output_file):
    length = len(dtm_list)
    density_avg = np.zeros(length, dtype=np.float32)
    tdc_avg = np.zeros(length, dtype=np.float32)

    for count in range(length):
        dtm_file = dtm_list[count]
        file_name = re.search('DTM(.+?).npy', dtm_file).group(1)[1:]

        start = time.time()
        print("Generating {} TTM ... ".format(file_name), flush=False)

        dtm = np.load(dtm_file)
        size = dtm.shape[1]
        tdm = dtm.T
        cos = 1 - pdist(tdm, 'cosine')
        ttm = squareform(cos)
        for i in range(size):
            ttm[i][i] = 1

        with open("../data/TTM/{}.npy".format(file_name), 'wb+') as f:
            np.save(f, ttm)
        print("finished in {:.2f} sec.".format(time.time() - start), flush=True)

        print("Computing {} TDC  ... ".format(file_name), flush=False)

        density, tdc = compute(ttm, size)
        density_avg[count] = density
        tdc_avg[count] = np.mean(tdc)
        with open("../data/TDC/{}.npy".format(file_name), 'wb+') as f:
            np.save(f, tdc)

        duration = float("{0:.2f}".format(time.time() - start))
        try:
            log_file.write("{}\t{}\t{}\n".format(file_name, str(ttm.shape), str(duration)))
            print("finished in {:.2f} sec.".format(time.time() - start), flush=True)
        except Exception:
            print("Failed to log {}".format(file_name))
            raise

    with open("../data/density{}.npy".format(output_file), 'wb+') as f:
        np.save(f, density_avg)

    with open("../data/tdc{}.npy".format(output_file), 'wb+') as f:
        np.save(f, tdc_avg)


def getJournals():
    with open('../data/journals.txt', encoding='utf-8') as f:
        line = f.readline()
        journals_name = line.split(',')
        journals_path = []
        for journal in journals_name:
            journals_path.append("../data/DTM/{}.npy".format(journal))
        return journals_path


if __name__ == '__main__':
    log_file = open('../log/TDC.txt', 'a+', encoding='utf-8')
    log_file.write("File_name\tTTM_shape\tduration\n")

    dtm_by_journal_list = getJournals()
    dtm_by_py_list = glob.glob('../data/DTM/*[0-9].npy')
    if len(dtm_by_py_list) > 0:
        main(dtm_by_py_list, output_file="_by_py")
    else:
        raise Exception('No matching files group by py')

    # main(dtm_by_journal_list, output_file="_by_journal")

    log_file.close()
