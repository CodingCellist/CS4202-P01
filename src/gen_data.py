import argparse
import os
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

from always_taken import always_taken
from two_bit_prediction import two_bit_prediction
from gshare import gshare
from profiled1 import profiled_1
from profiled2 import profiled_2


def gen_data(dirpath, outfile, nThreads=1):
    with ProcessPoolExecutor(max_workers=nThreads) as executor:
        manager = mp.Manager()
        lock = manager.Lock()
        with open(outfile, mode='a') as csvfile:
            csvfile.write('predictor,accuracy\n')
        for f in sorted(os.listdir(dirpath)):
            infile = dirpath + f
            executor.submit(fn=always_taken,
                            infile=infile, outfile=outfile, lock=lock)
            executor.submit(fn=gshare,
                            infile=infile, outfile=outfile, lock=lock)
            for table_size in [512, 1024, 2048, 4096]:
                executor.submit(fn=two_bit_prediction,
                                infile=infile, table_size=table_size,
                                outfile=outfile, lock=lock)
                executor.submit(fn=profiled_1,
                                infile=infile, table_size=table_size,
                                outfile=outfile, lock=lock)
                executor.submit(fn=profiled_2,
                                infile=infile, table_size=table_size,
                                outfile=outfile, lock=lock)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath", type=str,
                        help="The path to the directory containing input files.")
    parser.add_argument("outfile", type=str,
                        help="The file to output the result to. Must be a CSV"
                             " file.")
    parser.add_argument("-t", "--threads", type=int, default=1,
                        help="The maximum number of threads to use.")
    args = parser.parse_args()

    if not args.outfile.endswith(".csv"):
        raise argparse.ArgumentTypeError("The output must be a .csv file.")

    gen_data(args.dirpath, args.outfile, nThreads=args.threads)
