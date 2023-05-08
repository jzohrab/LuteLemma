import sys
import os
from lutelemma.lemmatize import Hello

ARGS=sys.argv
if (len(ARGS) != 3):
    print("Need lang code, infile")
    sys.exit(1)

langcode = ARGS[1]
infile = ARGS[2]

if (not os.path.exists(infile)):
    print(f"Missing input file {infile}")
    sys.exit(1)

print(langcode)
print(infile)

h = Hello()
h.hi()
