import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--size", type=int, default=512,
                    help="The size of the address table. Must be 512, 1024,"
                         " 2048, or 4096.")
parser.add_argument("infile", type=str, help="The path to the input file.")
args = parser.parse_args()

table_size = args.size

if table_size not in [512, 1024, 2048, 4096]:
    raise argparse.ArgumentTypeError("size must be one of 512, 1024, 2048, or 4096.")

with open(args.infile) as branch_file:
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

    branch_file.seek(0)
    # predicting
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
    print("Branches: {:d}\nHits: {:d}\nHit rate: {:4.3f}%"
          .format(branches, hits, hit_rate * 100))
