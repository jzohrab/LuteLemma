# Lute Lemma

A simple python 3.11 script to generate child-parent lemma mappings for import into [Lute](https://github.com/jzohrab/lute).

This uses [spaCy-stanza](https://github.com/explosion/spacy-stanza), a wrapper around [Stanza](https://github.com/stanfordnlp/stanza) (formerly StanfordNLP) to find lemma.  Stanza has models for over 60 languages, see [this page](https://stanfordnlp.github.io/stanza/available_models.html) for the complete list.

For example, given the following Spanish input file (in demo/es_input.txt):

```
perros
perro
perras
vives
vivimos
vivieron
muchacho
muchacha
coches
vez
```

The script generates a file containing the following commented file, where the first column is the original term and the second is a root, or lemma, form:

```
### 3 single child parents:
coches	coche
perras	perra
perros	perro

### 1 multi-child parents:

# Length 5 (1 parents):
# vivir (3 children)
vives	vivir
vivieron	vivir
vivimos	vivir
```

Only cases where the lemma form differs from the original term are included, so this doesn't show the terms `muchacho`, `vez`, `que`, etc.

_(If you know Spanish, you'll see that some of the above aren't really useful ... but the spaCy pipeline is often very, very good.)_

## Requirements

* python3.11 (perhaps will work with earlier versions, untested)

## Installation

Use pip3.11:

```
python3.11 -m venv .env
pip3.11 install -r requirements.txt
```

## Usage:

```
$ source .env/bin/activate

# Ignore warnings with -W ignore
#
# 1st arg: Stanza language code of the terms (link below)
# 2nd arg: path to input file
# 3rd arg: path to the output file
#
$ python3.11 -W ignore main.py es demo/es_input.txt output.txt
Opening library ...
Done.
Loading pipeline ...
Done.  Processing 1 batches.
  1 of 1

File generated: output_1.txt

Please remove any mappings you don't want from this file before importing it.
```

 Stanza language codes: Stanza has models for over 60 languages, see [this page](https://stanfordnlp.github.io/stanza/available_models.html) for the complete list.
 
## Refs

- https://github.com/explosion/spacy-stanza
- https://stanfordnlp.github.io/stanza/download_models.html
- https://github.com/jzohrab/lute