import sys
import os

ARGS=sys.argv
if (len(ARGS) != 2):
    print("Need infile")
    sys.exit(1)

infile = ARGS[1]

if (not os.path.exists(infile)):
    print(f"Missing input file {infile}", {infile: 'bla'})
    sys.exit(1)

f = open(infile, 'r')
lines = [ lin.split("\t") for lin in f.readlines() ]
by_parent_length = sorted(
    lines,
    key=lambda x: '_'.join([ '%03d' % len(x[1]), x[1], x[0] ])
)

outfile=infile + '.sorted'
print(f"Writing to {outfile}")

with open(outfile, 'w') as writer:
    for p in by_parent_length:
        writer.write(f"{p[0]}\t{p[1]}")

print(f"\nFile generated:\n{outfile}\n\n")
print("Please remove any unwanted mappings from the file before importing.")
