import sys
import os

ARGS=sys.argv
if (len(ARGS) != 3):
    print("Need lang code, infile")
    sys.exit(1)

langcode = ARGS[1]
infile = ARGS[2]

if (not os.path.exists(infile)):
    print(f"Missing input file {infile}", {infile: 'bla'})
    sys.exit(1)

f = open(infile, 'r')
lines = f.readlines()

# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
# Yield successive n-sized
# chunks from arr.
def divide_chunks(arr, n):
    # looping till length arr
    for i in range(0, len(arr), n):
        yield arr[i:i + n]

linegroups = list(divide_chunks(lines, 100))
groups = [ ''.join(g).strip() for g in linegroups ]


print("Opening library ...")
from spacy_stanza import load_pipeline
print("Done.")

currdir = os.path.dirname(os.path.abspath(__file__))
downloaddir = os.path.join(currdir, 'models')
langcode="es"
langdir=os.path.join(downloaddir, langcode)

if (not os.path.exists(downloaddir)):
    os.mkdir(downloaddir)

# if (not os.path.exists(langdir)):
#     print(f'Path {langdir} exists, model already downloaded.')

if (not os.path.exists(langdir)):
    print(f"downloading {langcode} model to {langdir}")
    import stanza
    stanza.download(langcode, model_dir=downloaddir, processors="tokenize,mwt,pos,lemma")
    print("Done.")

print("Loading pipeline ...")
nlp = load_pipeline(    
    langcode,
    dir=downloaddir,
    processors="tokenize,mwt,pos,lemma",
    download_method=None,
    logging_level='FATAL'
)
print("Done.")

outfile=infile + '.import'
print(f"Writing to {outfile}")

n = 0
numgroups = len(groups)
with open(outfile, 'w') as writer:
    for text in groups:
        n += 1
        print(f'  {n} of {numgroups}')
        doc = nlp(text)
        lemmatized = [ token for token in doc if token.text != token.lemma_ ]
        child_parent = [ [ token.text, token.lemma_ ] for token in lemmatized ]
        by_parent_length = sorted(child_parent, key=lambda x: len(x[1]))

        for p in by_parent_length:
            writer.write(f"{p[0]}\t{p[1]}\n")

        writer.flush()

print(f"\nFile generated:\n{outfile}\n\n")
print("Please remove any unwanted mappings from the file before importing.")
