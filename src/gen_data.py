import argparse
import os
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

from always_taken import always_taken
from two_bit_prediction import two_bit_prediction
from gshare import gshare
from profiled1 import profiled_1
from profiled2 import profiled_2


def gen_data(dirpath, outfile, n_threads=1, set_size=10):
    with ProcessPoolExecutor(max_workers=n_threads) as executor:
        manager = mp.Manager()
        lock = manager.Lock()
        with open(outfile, mode='a') as csvfile:
            csvfile.write('set,predictor,accuracy\n')
        i = 0
        setnumb = 0
        for f in sorted(os.listdir(dirpath)):
            if i == set_size:
                i = 0
                setnumb += 1
            infile = dirpath + f
            executor.submit(fn=always_taken,
                            infile=infile, outfile=outfile, lock=lock, setnumb=setnumb)
            executor.submit(fn=gshare,
                            infile=infile, outfile=outfile, lock=lock, setnumb=setnumb)
            for table_size in [512, 1024, 2048, 4096]:
                executor.submit(fn=two_bit_prediction,
                                infile=infile, table_size=table_size,
                                outfile=outfile, lock=lock, setnumb=setnumb)
                executor.submit(fn=profiled_1,
                                infile=infile, table_size=table_size,
                                outfile=outfile, lock=lock, setnumb=setnumb)
                executor.submit(fn=profiled_2,
                                infile=infile, table_size=table_size,
                                outfile=outfile, lock=lock, setnumb=setnumb)
            i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath", type=str,
                        help="The path to the directory containing input files.")
    parser.add_argument("outfile", type=str,
                        help="The file to output the result to. Must be a CSV"
                             " file.")
    parser.add_argument("-t", "--threads", type=int, default=1,
                        help="The maximum number of threads to use. Default is 1.")
    parser.add_argument("--setsize", type=int, default=10,
                        help="The number of files in a set (if multiple files"
                             " were generated per input). Default is 10.")
    args = parser.parse_args()

    if not args.outfile.endswith(".csv"):
        raise argparse.ArgumentTypeError("The output file must be a .csv file.")
    if not args.setsize >= 0:
        raise argparse.ArgumentTypeError("The setsize must be >= 0.")

    gen_data(args.dirpath, args.outfile,
             n_threads=args.threads, set_size=args.setsize)
