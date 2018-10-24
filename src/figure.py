import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import re
import glob


def main():
    tdc_list = glob.glob('../TDC/*.npy')
    count = 0

    for tdc_file in tdc_list:
        if count < 1:
            file_name = re.search('TDC(.+?).npy', tdc_file).group(1)[1:]
            count += 1

            start = time.time()
            print("Drawing %s TDC ... " % file_name, flush=True)

            tdc = np.load(tdc_file)

            size = len(tdc)
            print("Size of {} is: {}".format(file_name, size))

            x = np.arange(size)
            plt.scatter(x, tdc, marker='.', linewidths=0.8)
            plt.show()

            print("finished in {:.2f} sec.".format(time.time() - start), flush=True)


if __name__ == '__main__':
    main()
