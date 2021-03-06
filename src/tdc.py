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
import gc


def compute():
    start_time = time.time()
    print("Generating {} {} TTM ... ".format(FIELD, time_flag), flush=False)

    dtm = np.load(dtm_file)
    size = dtm.shape[1]
    tdm = dtm.T

    del dtm
    gc.collect()

    cos = 1 - pdist(tdm, 'cosine')

    del tdm
    gc.collect()

    # cos = pdist(tdm, 'cosine')
    ttm = squareform(cos)
    for i in range(size):
        ttm[i][i] = 1

    del cos, i
    gc.collect()

    print("finished in {:.2f} sec.".format(time.time() - start_time), flush=True)

    print("Computing {} {} TDC ... ".format(FIELD, time_flag), flush=False)

    centroid = np.mean(ttm, axis=0)
    dist = np.float32(0)
    c = np.float64(1.3)  # stable
    for i in range(size):
        # cosine distance
        # dist[i] = np.dot(ttm[i, :], centroid)/(np.linalg.norm(ttm[i, :])*(np.linalg.norm(centroid)))
        # edu distance
        dist += 1 / (math.pow(c, np.linalg.norm(ttm[i, :] - centroid)))
    density = dist / size

    del i, dist, centroid
    gc.collect()

    density_t_list = []
    for i in range(size):
        dist_t = np.float(0)
        ttm_t = ttm.copy()
        ttm_t[i, :] = np.zeros(size)
        ttm_t[:, i] = np.zeros(size)
        centroid_i = np.sum(ttm_t, axis=0) / (size - 1)
        for j in range(size):
            if j != i:
                dist_t += 1 / (math.pow(c, np.linalg.norm(ttm_t[j, :] - centroid_i)))
        density_t_list.append(dist_t / (size - 1))
        if i % 2000 == 0:
            print(i, 'It is coming soon~~~', time.time() - start_time)

        del ttm_t, centroid_i, dist_t
        gc.collect()

    del i, ttm
    gc.collect()

    density_t_array = np.array(density_t_list)
    density_avg = np.mean(np.fabs(density_t_array - density))
    # print('density_avg\n', np.sum(density_t_array), density_avg)
    tdc = (density_t_array - density) / density_avg

    # print('tdc\n', tdc[0: 10])

    del density_t_list, density_t_array, density_avg
    gc.collect()

    with open("../data/TDC/{}-tdc-{}.npy".format(FIELD, time_flag), 'wb+') as f:
        np.save(f, tdc)

    duration = float("{0:.2f}".format(time.time() - start_time))
    try:
        log_file.write("{}-{}\t{}\t{}\t{}\n".format(FIELD, time_flag, size, duration))
        print("finished in {:.2f} sec.".format(duration), flush=True)
    except Exception:
        print("Failed to log {} {}".format(FIELD, time_flag))
        raise


if __name__ == '__main__':
    # FIELDS = ['IS', 'CS', 'MS']
    FIELDS = ['IS-CS-MS']
    # FIELDS = ['IS']
    PYS = 5
    py_list = []
    time_flag = ''
    for FIELD in FIELDS:
        log_file = open('../log/{}-TDC-log.txt'.format(FIELD), 'a+', encoding='utf-8')
        log_file.write("Type\tLength of term\tdensity\tduration\n")
        
        if PYS == 1:
            py_list = np.arange(2017, 2018, 1)
            time_flag = '17'
        elif PYS == 5:
            py_list = np.arange(2013, 2018, 1)
            time_flag = '13-17'

        dtm_file = "../data/DTM/{}-dtm-{}.npy".format(FIELD, time_flag)
        # with open(dtm_file, 'wb+') as f:
        #     dtm_test = np.arange(0, 10000, 0.1).reshape(100, 1000)
        #     np.save(f, dtm_test)

        compute()

        log_file.close()
