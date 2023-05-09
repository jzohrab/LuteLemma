import os

def build_dict(arr):
    d = dict()
    for pair in arr:
        child, parent = pair
        if parent not in d:
            d[parent] = []
        if child not in d[parent]:
            d[parent].extend([child])
    return d

def single_child_parents(d):
    ps = [ k for k, v in d.items() if len(v) == 1 ]
    return ps

def multi_child_parents(d):
    ps = [ k for k, v in d.items() if len(v) > 1 ]
    return ps

def get_output_array(d):
    arr = []
    scp = sorted(single_child_parents(d))
    arr.extend([f"### {len(scp)} single child parents:"])
    for p in scp:
        c = d[p][0]
        arr.extend([f"{c}\t{p}"])
    arr.extend([""])

    ps = multi_child_parents(d)
    arr.extend([f"### {len(ps)} multi-child parents:"])
    lengths = set([ len(p) for p in ps ])
    for length in lengths:
        plen = [ p for p in ps if len(p) == length ]
        plen = sorted(plen)
        arr.extend([''])
        arr.extend([f"# Length {length}:"])
        for p in plen:
            arr.extend([f"# {p} ({len(d[p])} children)"])
            for c in sorted(d[p]):
                arr.extend([f"{c}\t{p}"])

    return arr


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
    d = build_dict(arr)
    outarr = get_output_array(d)
    for lin in outarr:
        writer.write(f"{lin}\n")
    writer.flush()
