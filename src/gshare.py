import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str, help="The path to the input file.")
args = parser.parse_args()

table_size = 256    # 2^8, because the GR is 8 bits

with open(args.infile) as branch_file:
    gr = 0
    table = {}
    keys = []
    branches = 0
    hits = 0
    for l in branch_file:
        branches += 1
        pc = int(l.split(' ')[0][-3:])
        taken = int(l.split(' ')[1])
        gr = (gr << 1) + taken
        key = gr ^ pc
        if key not in keys:
            if len(keys) == table_size:
                table.pop(keys[0])
                keys = keys[1:]
            keys.append(key)
            table[key] = 0
        assert len(table) <= table_size
        value = table.get(key)

        # prediction
        if value == 3 or value == 2:
            prediction = "1\n"
        elif value == 1 or value == 0:
            prediction = "0\n"

        # two-bit update
        if value == 3:
            if l.endswith(prediction):  # if we are right, i.e. taken
                hits += 1
            else:
                table[key] = 2
        elif value == 2:
            if l.endswith(prediction):  # if we are right, i.e. taken
                hits += 1
                table[key] = 3
            else:
                table[key] = 0
        elif value == 1:
            if l.endswith(prediction):  # if we are right, i.e. not taken
                hits += 1
                table[key] = 0
            else:
                table[key] = 3
        elif value == 0:
            if l.endswith(prediction):  # if we are right, i.e. not taken
                hits += 1
            else:
                table[key] = 1
    hit_rate = hits / branches
    print("Branches: {:d}\nHits: {:d}\nHit rate: {:4.3f}%"
          .format(branches, hits, hit_rate * 100))
