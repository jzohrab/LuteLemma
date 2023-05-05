import sys
import os

ARGS=sys.argv
if (len(ARGS) != 3):
    print("Need lang code, infile")
    sys.exit(1)

langcode = ARGS[1]
infile = ARGS[2]

if (not os.path.exists(infile)):
    print(f"Missing input file {infile}")
    sys.exit(1)

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

f = open(infile, 'r')
text = f.read()
# text = """
# Los acomodé contra las paredes, pensando en la comodidad y no en la estética.
# """

print("Loading pipeline ...")
nlp = load_pipeline(    
    langcode,
    dir=downloaddir,
    processors="tokenize,mwt,pos,lemma",
    download_method=None,
    logging_level='FATAL'
)
print("Done.  Processing doc ...")
doc = nlp(text)
print("Done.")

lemmatized = [ token for token in doc if token.text != token.lemma_ ];
for token in lemmatized:
    print(token.text, token.lemma_)
