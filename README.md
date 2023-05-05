Example using spaCy and Stanza to lemmatize items.

```
python3.11 -m venv .env
pip3.11 install -r requirements.txt

source .env/bin/activate

# The call.
# Ignore warnings with -W ignore
# 1st arg: language code of the file
# 2nd arg: file
python3.11 -W ignore lemmatize.py es path/to/input/file

deactivate
```


Refs

- https://github.com/explosion/spacy-stanza
- https://pypi.org/project/spacy-stanza/
- https://stanfordnlp.github.io/stanza/download_models.html
- https://stanfordnlp.github.io/stanza/pipeline.html#pipeline
- https://stanfordnlp.github.io/stanza/pipeline.html#processors

- https://medium.com/@BioCatchTechBlog/passing-arguments-to-a-docker-container-299d042e5ce