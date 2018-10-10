import sys

lines = 0
taken = 0

with open(sys.argv[1]) as branch_file:
    for i in branch_file:
        lines += 1
        if i.endswith("1\n"):
            taken += 1

print("Lines:", lines, "\t taken:", taken)
print("Hit rate: {:4.3f}%".format(taken/lines * 100))
