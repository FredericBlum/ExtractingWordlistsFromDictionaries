"""
Map concepts to concepticon.
"""

import argparse
import csv
from collections import defaultdict

from cldfbench.cli_util import add_catalog_spec
from clldutils.clilib import Table, add_format
from pycldf import Dataset
from pyconcepticon import Concepticon
from pysem.glosses import to_concepticon


def main(*args):

    parser = argparse.ArgumentParser(description='Conceptlist Mapping')
    add_catalog_spec(parser, 'concepticon')
    add_format(parser, default="simple")
    parser.add_argument("--data", default="cldf/Dictionary-metadata.json")
    parser.add_argument("--conceptlist", default="Dellert-2018-1016")
    parser.add_argument("--language", default="en")
    parser.add_argument("--output", default="raw/conceptlist.tsv")
    args = parser.parse_args(*args)

    concepticon = Concepticon(args.concepticon)

    clist = {
        c.concepticon_id: c
        for c in concepticon.conceptlists[args.conceptlist].concepts.values()
        if c.concepticon_gloss}
    ds = Dataset.from_metadata(args.data)
    mapped = defaultdict(list)
    entries = defaultdict(list)
    for sense in ds.objects("SenseTable"):
        entry = sense.entries[0]
        entries[entry.cldf.headword].append(sense.cldf.description)
        pos = entry.cldf.partOfSpeech.split(",")[0] if entry.cldf.partOfSpeech else ""
        maps = to_concepticon(
            [{"gloss": sense.cldf.description, "pos_ref": pos}],
            language=args.language)
        if maps[sense.cldf.description]:
            cid, cgl, _, score = maps[sense.cldf.description][0]
            if cid in clist:
                mapped[cid, cgl].append(
                    [sense.id, sense.cldf.description, entry.cldf.headword])
    table = []
    visited = set()
    for k, values in mapped.items():
        for sense_id, sense, form in values:
            table.append([
                k[0], k[1], form, "; ".join(entries.get(form, [""])), sense,
                sense_id])
        visited.add(k[0])
    for idx, concept in clist.items():
        if idx not in visited:
            table.append([idx, concept.concepticon_gloss, "", "", "", ""])

    table.sort(key=lambda x: x[1])
    with Table(
        args, "ID", "CONCEPTICON_ID", "CONCEPTICON_GLOSS",
        "FORM", "MEANING", "SENSE", "SENSE_ID"
    ) as tbl:
        for row_no, row in enumerate(table, 1):
            tbl.append([row_no] + row)
    with open(args.output, "w") as f:
        wtr = csv.writer(f, delimiter="\t")
        wtr.writerow([
            "ID", "CONCEPTICON_ID", "CONCEPTICON_GLOSS", "FORM", "MEANING",
            "SENSE", "SENSE_ID"])
        wtr.writerows(
            [row_no] + row
            for row_no, row in enumerate(table, 1))
