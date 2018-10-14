import argparse


def always_taken(infile, outfile=None, lock=None):
    with open(infile) as branch_file:
        branches = 0
        hits = 0
        for l in branch_file:
            branches += 1
            if l.endswith("1\n"):
                hits += 1
    hit_rate = hits / branches
    if outfile is None:
        print("Branches: {:d}\nHits: {:d}\nHit rate: {:4.3f}%"
              .format(branches, hits, hit_rate * 100))
    else:
        if lock is not None:
            lock.acquire()
            with open(outfile, mode='a') as csvfile:
                csvfile.write('"{:s}",{:.3f}\n'
                              .format('always-taken', hit_rate * 100))
            lock.release()
        else:
            with open(outfile, mode='a') as csvfile:
                csvfile.write('"{:s}",{:.3f}\n'
                              .format('always-taken', hit_rate * 100))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, help="The path to the input file.")
    parser.add_argument("-o", "--outfile", type=str, default=None,
                        help="The file to output the result to. Must be a CSV"
                             " file.")
    args = parser.parse_args()

    if args.outfile is not None:
        if not args.outfile.endswith(".csv"):
            raise argparse.ArgumentTypeError("The output must be a .csv file.")

    always_taken(args.infile, outfile=args.outfile)
