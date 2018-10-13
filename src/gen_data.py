import argparse
import os

from always_taken import always_taken
from two_bit_prediction import two_bit_prediction
from gshare import gshare
from profiled1 import profiled_1
from profiled2 import profiled_2


def gen_data(dirpath, outfile):
    with open(outfile, mode='a') as csvfile:
        csvfile.write('predictor,accuracy\n')
    for f in sorted(os.listdir(dirpath)):
        infile = dirpath + f
        always_taken(infile, outfile)
        gshare(infile, outfile)
        for table_size in [512, 1024, 2048, 4096]:
            two_bit_prediction(infile, table_size, outfile)
            profiled_1(infile, table_size, outfile)
            profiled_2(infile, table_size, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dirpath", type=str,
                        help="The path to the directory containing input files.")
    parser.add_argument("outfile", type=str,
                        help="The file to output the result to. Must be a CSV"
                             " file.")
    args = parser.parse_args()

    if not args.outfile.endswith(".csv"):
        raise argparse.ArgumentTypeError("The output must be a .csv file.")

    gen_data(args.dirpath, args.outfile)
