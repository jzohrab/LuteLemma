import sys
import os
from lutelemma.lemmatize import generate_import

ARGS=sys.argv
if (len(ARGS) != 5):
    print("Need lang name, code, infile, outfile")
    sys.exit(1)

language_name = ARGS[1]
langcode = ARGS[2]
infile = ARGS[3]
outfile = ARGS[4]

if (not os.path.exists(infile)):
    print(f"Missing input file {infile}")
    sys.exit(1)

lines = []
with open(infile, 'r') as reader:
    lines = [line.lower() for line in reader]

with open(outfile, 'w') as writer:
    generate_import(language_name, langcode, lines, writer)

print(f"\nFile generated: {outfile}")
print("\nPlease remove any mappings you don't want from this file before importing it.")
