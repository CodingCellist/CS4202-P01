import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str, help="The path to the input file.")
args = parser.parse_args()

with open(args.infile) as branch_file:
    branches = 0
    hits = 0
    for l in branch_file:
        branches += 1
        if l.endswith("1\n"):
            hits += 1
print("Branches: {:d}\nHits: {:d}\nHit rate: {:4.3f}%"
      .format(branches, hits, hits / branches * 100))
