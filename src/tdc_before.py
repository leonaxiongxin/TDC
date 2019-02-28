"""
  tdc.py
  Convert Document-Term Matrix to Term-Term matrix
  Compute the TDC of each term
  Compute the average value
  Via cosine similarity
"""
import time
import numpy as np
from scipy.spatial.distance import pdist, squareform
import math


def compute():
    start_time = time.time()
    print("Generating {} {} TTM ... ".format(FIELD, time_flag), flush=False)

    dtm = np.load(dtm_file)
    size = dtm.shape[1]
    tdm = dtm.T
    cos = 1 - pdist(tdm, 'cosine')
    # cos = pdist(tdm, 'cosine')
    ttm = squareform(cos)
    for i in range(size):
        ttm[i][i] = 1

    # with open("../data/TTM/{}-ttm-{}.npy".format(FIELD, time_flag), 'wb+') as f:
    #     np.save(f, ttm)

    print("finished in {:.2f} sec.".format(time.time() - start_time), flush=True)

    # print("Loading {} {} TTM ... ".format(FIELD, time_flag), flush=False)
    # ttm = np.load("../data/TTM/{}-ttm-{}.npy".format(FIELD, time_flag))
    # size = ttm.shape[0]
    # print("finished in {:.2f} sec.".format(time.time() - start_time), flush=True)

    print("Computing {} {} TDC ... ".format(FIELD, time_flag), flush=False)

    centroid = np.mean(ttm, axis=0)
    dist = np.zeros(size, dtype=np.float32)
    c = np.float64(1.3)  # stable
    for i in range(size):
        # cosine distance
        # dist[i] = np.dot(ttm[i, :], centroid)/(np.linalg.norm(ttm[i, :])*(np.linalg.norm(centroid)))
        # edu distance
        dist[i] = 1 / (math.pow(c, np.linalg.norm(ttm[i, :] - centroid)))
    density = np.mean(dist)

    dist_t = np.zeros(size - 1, dtype=np.float32)
    density_t = np.zeros(size, dtype=np.float32)
    for i in range(size):
        ttm_c = np.delete(ttm, i, axis=0)
        ttm_t = np.delete(ttm_c, i, axis=1)
        centroid_i = np.mean(ttm_t, axis=0)
        for j in range(size - 1):
            # dist_t[j] = np.dot(ttm_t[j, :], centroid_i)/(np.linalg.norm(ttm_t[j, :])*(np.linalg.norm(centroid_i)))
            dist_t[j] = 1 / (math.pow(c, np.linalg.norm(ttm_t[j, :] - centroid_i)))
        density_t[i] = np.mean(dist_t)

    density_avg = np.mean(np.fabs(density_t - density))
    # print('density_avg\n', np.sum(density_t), density_avg)
    tdc = (density_t - density) / density_avg

    print('tdc\n', tdc[0: 10])

    with open("../data/TDC/{}-tdc-{}.npy".format(FIELD, time_flag), 'wb+') as f:
        np.save(f, tdc)

    duration = float("{0:.2f}".format(time.time() - start_time))
    try:
        log_file.write("{}-{}\t{}\t{}\t{}\n".format(FIELD, time_flag, size, density_avg, duration))
        print("finished in {:.2f} sec.".format(duration), flush=True)
    except Exception:
        print("Failed to log {} {}".format(FIELD, time_flag))
        raise


if __name__ == '__main__':
    # FIELDS = ['IS', 'CS', 'MS']
    # FIELDS = ['IS-CS-MS']
    FIELDS = ['IS']
    PYS = 1
    py_list = []
    time_flag = ''
    for FIELD in FIELDS:
        log_file = open('../log/{}-TDC-before.txt'.format(FIELD), 'a+', encoding='utf-8')
        log_file.write("Type\tLength of term\tdensity\tduration\n")

        if PYS == 1:
            py_list = np.arange(2017, 2018, 1)
            time_flag = '17-ori'
        elif PYS == 5:
            py_list = np.arange(2013, 2018, 1)
            time_flag = '13-17'

        dtm_file = "../data/DTM/{}-dtm-{}.npy".format(FIELD, time_flag)
        # with open(dtm_file, 'wb+') as f:
        #     dtm_test = np.arange(0, 10000, 0.1).reshape(100, 1000)
        #     np.save(f, dtm_test)
        compute()

        log_file.close()
