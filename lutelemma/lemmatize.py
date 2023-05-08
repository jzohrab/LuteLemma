import os

# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
# Yield successive n-sized
# chunks from arr.
def divide_chunks(arr, n):
    # looping till length arr
    for i in range(0, len(arr), n):
        yield arr[i:i + n]


def get_child_parent_pairs(langcode, lines):
    linegroups = list(divide_chunks(lines, 100))
    groups = [ ''.join(g).strip() for g in linegroups ]

    print("Opening library ...")
    from spacy_stanza import load_pipeline
    print("Done.")

    currdir = os.path.dirname(os.path.abspath(__file__))
    downloaddir = os.path.join(currdir, '..', 'models')
    langdir=os.path.join(downloaddir, langcode)

    if (not os.path.exists(downloaddir)):
        os.mkdir(downloaddir)

    if (not os.path.exists(langdir)):
        print(f'Path {langdir} exists, model already downloaded.')

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
    print(f"Done.  Processing {len(groups)} batches.")

    ret = []
    n = 0
    numgroups = len(groups)
    for text in groups:
        n += 1
        print(f'  {n} of {numgroups}')
        doc = nlp(text)
        child_parent = [
            [ token.text.strip(), token.lemma_.strip() ]
            for token in doc if token.text.strip() != ''
        ]
        ret.extend([ p for p in child_parent if p[0] != p[1] ])

    return ret


def generate_import(langcode, lines, writer):
    arr = get_child_parent_pairs(langcode, lines)
    # print(arr)
    by_parent_length = sorted(
        arr,
        key=lambda x: '_'.join([ '%03d' % len(x[1]), x[1], x[0] ])
    )
    for p in by_parent_length:
        writer.write(f"{p[0]}\t{p[1]}\n")
