# Resource acquisition for understudied languages: Extracting wordlists from dictionaries for computer-assisted language comparison

## Summary

This repository contains all the data and code that was used for the initial submission of the paper. The following guidelines should make it possible to reproduce the workflow of the two case studies.

## Necessary packages

All the code makes the general assumption that you have Python and Git installed on your computer. As for the project-specific requirements, we lead you through the installation process. We include the `getcl`-package in this repository during the review process. Please install all the necessary packages using the following code:

```shell
pip install -r requirements.txt
```

On Windows, you might need to prefix the `pip` command with `python -m`.
In order to run the code, you will need local copies of CLTS, Concepticon, and Glottolog. To prepare those reference catalogues, plesae run the followign code and follow the interactive prompts:

```shell
cldfbench catconfig
```

You are now ready to reproduce the case-studies.

## Case Study I: Daakaka

To reproduce the first case study, please switch to the respective working directory.

```shell
cd vonprincedaakaka
```

In this repository, you find three main folder: raw/, etc/, and cldf/. The raw-folder contains the raw data before mapping and pre-processing, the etc/ fodler the metadata used during the converison, and the cldf/-folder the converted files using the Cross-Linguistic Data Formats (CLDF). To re-run the mapping of concepts, please use the following code:

```shell
conceptlist --data=cldf/Dictionary-metadata.json --conceptlist=Swadesh-1955-100 --concepticon-version=v3.2.0 --language=en --output=raw/raw_automap.tsv
```

The result are the automatically mapped concepts. We recommend to now run a manual check of all mappings, since there are some cases which can be difficult to map due to homonymy (e.g. 'bark' or 'lie'). We have done such a manual check and saved the file as `raw_filtermap.tsv`. This is the file that we use as an input to the final CLDF run.

```shell
cldfbench lexibank.makecldf cldfbench_daakaka.py --concepticon-version=v3.2.0 --glottolog-version=v5.0 --clts-version=v2.2.0
```

## Case Study II: Amahuaca

The workflow for Amahuaca is very similar, except that there is one additional step previous to the mapping: The parsing of the raw data, stored in `hydeamahuaca/raw/parsing/`. You can re-run the parsing using the following commands:

```shell
cd hydeamahuaca/raw/parsing
python parse.py
cd ../../
```

You have now the data as csv-file, which you can convert to CLDF. Again, you can run the mapping of the conceptlist with the following command.

```shell
conceptlist --data=cldf/Dictionary-metadata.json --conceptlist=Swadesh-1955-100 --concepticon-version=v3.2.0 --language=es --output=raw/raw_automap.tsv
```

Fllowing our workflow, we recommend to create a file that contains the manual check (`raw_filtermap.tsv`) and run the final CLDF conversion.

```shell
cldfbench lexibank.makecldf lexibank_hydeamahuaca.py --concepticon-version=v3.2.0 --glottolog-version=v5.0 --clts-version=v2.2.0
```
