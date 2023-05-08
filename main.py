import sys
import os
from lutelemma.lemmatize import generate_import

ARGS=sys.argv
if (len(ARGS) != 4):
    print("Need lang code, infile, outfile")
    sys.exit(1)

langcode = ARGS[1]
infile = ARGS[2]
outfile = ARGS[3]

if (not os.path.exists(infile)):
    print(f"Missing input file {infile}")
    sys.exit(1)

lines = []
with open(infile, 'r') as reader:
    lines = reader.readlines()

with open(outfile, 'w') as writer:
    generate_import(langcode, lines, writer)

print(f"\nFile generated: {outfile}")
