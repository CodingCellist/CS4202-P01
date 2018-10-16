import argparse


def profiled_1(infile, table_size, outfile=None, lock=None, setnumb=0):
    with open(infile) as branch_file:
        table = {}
        keys = []
        branches = 0
        hits = 0

        # profiling
        for l in branch_file:
            key = l.split(' ')[0][-3:]
            taken = int(l.split(' ')[1])
            if key not in keys:
                if len(keys) == table_size:
                    table.pop(keys[0])
                    keys = keys[1:]
                keys.append(key)
                table[key] = 0
            value = table[key]
            if taken == 1:
                table[key] = value + 1
            else:
                table[key] = value - 1

        # go back to start of file and predict
        branch_file.seek(0)
        for l in branch_file:
            branches += 1
            key = l.split(' ')[0][-3:]
            if key in keys:             # if we have the key, use the profiled history
                value = table[key]
                if value >= 0:
                    prediction = "1\n"
                else:
                    prediction = "0\n"
            else:
                prediction = "1\n"      # otherwise, predict always taken
            if l.endswith(prediction):
                hits += 1

        hit_rate = hits / branches
        if outfile is None:
            print("Branches: {:d}\nHits: {:d}\nHit rate: {:4.3f}%"
                  .format(branches, hits, hit_rate * 100))
        else:
            if lock is not None:
                lock.acquire()
                with open(outfile, mode='a') as csvfile:
                    csvfile.write('{:d},"{:s}-{:d}",{:.3f}\n'
                                  .format(setnumb, 'profiled-1', table_size, hit_rate * 100))
                lock.release()
            else:
                with open(outfile, mode='a') as csvfile:
                    csvfile.write('{:d},"{:s}-{:d}",{:.3f}\n'
                                  .format(setnumb, 'profiled-1', table_size, hit_rate * 100))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", type=int, default=512,
                        help="The size of the address table. Must be 512, 1024,"
                             " 2048, or 4096.")
    parser.add_argument("-o", "--outfile", type=str, default=None,
                        help="The file to output the result to. Must be a CSV"
                             " file.")
    parser.add_argument("infile", type=str, help="The path to the input file.")
    args = parser.parse_args()

    if args.size not in [512, 1024, 2048, 4096]:
        raise argparse.ArgumentTypeError(
            "size must be one of 512, 1024, 2048, or 4096.")
    if args.outfile is not None:
        if not args.outfile.endswith(".csv"):
            raise argparse.ArgumentTypeError("The output must be a .csv file.")

    profiled_1(args.infile, args.size, outfile=args.outfile)
