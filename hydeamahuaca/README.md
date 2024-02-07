# hydeamahuaca

## How to cite

If you use these data please cite
this dataset using the DOI of the [particular released version](../../releases/) you were using

## Description


This dataset is licensed under a CC-BY 4.0 license


Conceptlists in Concepticon:
- [Swadesh-1955-100](https://concepticon.clld.org/contributions/Swadesh-1955-100)
## Notes

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



## Statistics


![Glottolog: 100%](https://img.shields.io/badge/Glottolog-100%25-brightgreen.svg "Glottolog: 100%")
![Concepticon: 100%](https://img.shields.io/badge/Concepticon-100%25-brightgreen.svg "Concepticon: 100%")
![Source: 100%](https://img.shields.io/badge/Source-100%25-brightgreen.svg "Source: 100%")
![BIPA: 100%](https://img.shields.io/badge/BIPA-100%25-brightgreen.svg "BIPA: 100%")
![CLTS SoundClass: 100%](https://img.shields.io/badge/CLTS%20SoundClass-100%25-brightgreen.svg "CLTS SoundClass: 100%")

- **Varieties:** 1
- **Concepts:** 90
- **Lexemes:** 143
- **Sources:** 1
- **Synonymy:** 1.59
- **Invalid lexemes:** 0
- **Tokens:** 812
- **Segments:** 35 (0 BIPA errors, 0 CLTS sound class errors, 35 CLTS modified)
- **Inventory size (avg):** 35.00

## CLDF Datasets

The following CLDF datasets are available in [cldf](cldf):

- CLDF [Wordlist](https://github.com/cldf/cldf/tree/master/modules/Wordlist) at [cldf/cldf-metadata.json](cldf/cldf-metadata.json)
- CLDF [Dictionary](https://github.com/cldf/cldf/tree/master/modules/Dictionary) at [cldf/Dictionary-metadata.json](cldf/Dictionary-metadata.json)