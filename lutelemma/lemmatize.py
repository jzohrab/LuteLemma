import os
import csv


def build_dict(arr):
    d = dict()
    for pair in arr:
        parent, child = pair
        if parent not in d:
            d[parent] = []
        if child not in d[parent]:
            d[parent].extend([child])
    return d


def single_child_parents(d):
    ps = [k for k, v in d.items() if len(v) == 1]
    return ps


def multi_child_parents(d):
    ps = [k for k, v in d.items() if len(v) > 1]
    return ps


# Returns array:
# [ [ 'parent1' 'child1' ], [ 'p1', 'c2' ] ... ]
def get_parent_child_pairs(langcode, lines):
    print("Opening library ...")
    from spacy_stanza import load_pipeline
    print("Done.")

# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
# Yield successive n-sized
# chunks from arr.
    def divide_chunks(arr, n):
        for i in range(0, len(arr), n):
            yield arr[i : i + n]

    linegroups = list(divide_chunks(lines, 100))
    groups = ["".join(g).strip() for g in linegroups]


    currdir = os.path.dirname(os.path.abspath(__file__))
    downloaddir = os.path.join(currdir, "..", "models")
    langdir = os.path.join(downloaddir, langcode)

    if not os.path.exists(downloaddir):
        os.mkdir(downloaddir)

    if not os.path.exists(langdir):
        print(f"Path {langdir} exists, model already downloaded.")

    if not os.path.exists(langdir):
        print(f"downloading {langcode} model to {langdir}")
        import stanza

        stanza.download(
            langcode, model_dir=downloaddir, processors="tokenize,mwt,pos,lemma"
        )
        print("Done.")

    print("Loading pipeline ...")
    nlp = load_pipeline(
        langcode,
        dir=downloaddir,
        processors="tokenize,mwt,pos,lemma",
        download_method=None,
        logging_level="FATAL",
    )
    print(f"Done.  Processing {len(groups)} batches.")

    ret = []
    n = 0
    numgroups = len(groups)
    for text in groups:
        n += 1
        print(f"  {n} of {numgroups}")
        doc = nlp(text)
        child_parent = [
            [token.lemma_.strip(), token.text.strip()]
            for token in doc
            if token.text.strip() != ""
        ]
        ret.extend([p for p in child_parent if p[0] != p[1]])

    return ret


def generate_import(language_name, langcode, lines, writer):
    arr = get_parent_child_pairs(langcode, lines)

    d = build_dict(arr)

    csv_writer = csv.writer(writer)

    csv_writer.writerow(
        ["language", "term", "translation", "parent", "tags", "pronunciation"]
    )

    for parent, children in d.items():
        for child in children:
            csv_writer.writerow([language_name, child, "", parent, "", ""])

    writer.flush()
