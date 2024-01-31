## Reproduce parsing of dictionary

Within the lexibank-script: RUN = 'PRE'

```CLI
pip install -r cldf/requirements.txt
cldfbench lexibank.makecldf lexibank_hydeamahuaca.py --concepticon-version=v3.1.0 --glottolog-version=v4.8 --clts-version=v2.2.0
conceptlist --data=cldf/Dictionary-metadata.json --conceptlist=Swadesh-1955-100 --concepticon-version=v3.1.0 --language=es --output=raw/raw_mapped.tsv
```

Within the lexibank-script: RUN = 'FULL'

```CLI
cldfbench lexibank.makecldf lexibank_hydeamahuaca.py --concepticon-version=v3.1.0 --glottolog-version=v4.8 --clts-version=v2.2.0
```
