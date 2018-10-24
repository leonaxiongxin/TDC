"""
  tdc.py
  Convert Document-Term Matrix to Term-Term matrix
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


def main():
    dtm_list = glob.glob('../DTM/*.npy')
    flog = open('../TTMlog.txt', 'w+', encoding='utf-8')

    length = len(dtm_list)
    density = np.zeros(length, dtype=np.float32)

    for count in range(length):
        dtm_file = dtm_list[count]
        file_name = re.search('DTM(.+?).npy', dtm_file).group(1)[1:]

        start = time.time()
        print("Generating %s TTM ... " % file_name, flush=False)

        dtm = np.load(dtm_file)
        size = dtm.shape[1]
        tdm = dtm.T
        cos = 1 - pdist(tdm, 'cosine')
        ttm = squareform(cos)
        for i in range(size):
            ttm[i][i] = 1

        with open("../TTM/{}.npy".format(file_name), 'wb+') as f:
            np.save(f, ttm)
        print("finished in {:.2f} sec.".format(time.time() - start), flush=True)

        print("Computing %s TDC  ... " % file_name, flush=False)

        if count != 13 and count != 4:
            density_avg, tdc = compute(ttm, size)
            density[count] = density_avg
            with open("../TDC/{}.npy".format(file_name), 'wb+') as f:
                np.save(f, tdc)

            duration = float("{0:.2f}".format(time.time() - start))
            try:
                flog.write("{} \t {} \t {} \t {} \n".format(file_name, str(ttm.shape), str(density_avg), str(duration)))
                print("finished in {:.2f} sec.".format(time.time() - start), flush=True)
            except:
                print("Failed to log {}".format(file_name))
                raise
        else:
            density[count] = 0

    flog.close()
    with open("../density.npy", 'wb+') as f:
        np.save(f, density)


if __name__ == '__main__':
    main()
