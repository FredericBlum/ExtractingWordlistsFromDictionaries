# Resource acquisition for understudied languages: Extracting wordlists from dictionaries for computer-assisted language comparison

## Summary

This repository contains all the data and code that was used for the initial submission of the paper. The following guidelines should make it possible to reproduce the workflow of the two case studies.

## Necessary packages

We include the `getcl`-package in this repository during the review process. Please install all the necessary packages using the following code:

```CLI
pip install -r requirements.txt
pip install getcl/
```

In order to run the code, you will need local copies of CLTS, Concepticon, and Glottolog. To prepare those reference catalogues, plesae run the followign code and follow the interactive prompts:

```CLI
cldfbench catconfig
```

You are now ready to reproduce the case-studies.

## Case Study I: Daakaka

To reproduce the first case study, please switch to the respective working directory.

```CLI
cd vonprincedaakaka
```

In this repository, you find three main folder: raw/, etc/, and cldf/. The raw-folder contains the raw data before mapping and pre-processing, the etc/ fodler the metadata used during the converison, and the cldf/-folder the converted files using the Cross-Linguistic Data Formats (CLDF). To re-run the mapping of concepts, please use the following code:

```CLI
conceptlist --data=cldf/Dictionary-metadata.json --conceptlist=Swadesh-1955-100 --concepticon-version=v3.1.0 --language=en --output=raw/raw_mapped.tsv
```

You can now run the final CLDF conversion.

```CLI
cldfbench lexibank.makecldf cldfbench_daakaka.py --concepticon-version=v3.1.0 --glottolog-version=v4.8 --clts-version=v2.2.0
```

## Case Study II: Amahuaca

The workflow for Amahuaca is very similar, except that there is one additional step previous to the mapping: The parsing of the raw data, stored in `hydeamahuaca/raw/parsing/`. You can re-run the parsing using the following commands:

```CLI
cd hydeamahuaca/raw/parsing
python parse.py
cd ../../
```

You have now the data as csv-file, which you can convert to CLDF. Again, you can run both the mapping of the conceptlist and the conversion to CLDF using the following commands:

```CLI
conceptlist --data=cldf/Dictionary-metadata.json --conceptlist=Swadesh-1955-100 --concepticon-version=v3.1.0 --language=es --output=raw/raw_mapped.tsv
cldfbench lexibank.makecldf lexibank_hydeamahuaca.py --concepticon-version=v3.1.0 --glottolog-version=v4.8 --clts-version=v2.2.0
```
