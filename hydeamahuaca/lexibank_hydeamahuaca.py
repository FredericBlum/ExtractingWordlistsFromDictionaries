from collections import defaultdict
from pathlib import Path
import re
import attr
import pylexibank
from pylexibank import Lexeme
from pylexibank import Dataset as BaseDataset
from cldfbench import CLDFSpec
from clldutils.misc import slug

RUN = 'FULL'
# Set if mapping is re-run
# RUN = 'PRE'

@attr.s
class CustomLexeme(Lexeme):
    Meaning = attr.ib(default=None)
    Sense_ID = attr.ib(default=None)
    Entry_ID = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "hydeamahuaca"
    lexeme_class = CustomLexeme

    def cldf_specs(self):
        return {
            None: pylexibank.Dataset.cldf_specs(self),
            "dictionary": CLDFSpec(
                module="Dictionary",
                dir=self.cldf_dir,
            ),
        }

    def cmd_makecldf(self, args):
        senses = defaultdict(list)
        idxs = {}
        form2idx = {}

        for idx, row in enumerate(
            self.raw_dir.read_csv(
                "parsed_raw.tsv", delimiter="\t", dicts=True
                )
                ):
            # add idx and form2idx for dic based on extraction
            if row["GLOSS"].strip():
                fidx = str(idx+1)+"-"+slug(row["VALUE"])
                idxs[fidx] = row
                for sense in re.split("[,]", row["GLOSS"]):
                    if row["VALUE"] and sense:
                        senses[slug(sense, lowercase=False)] += [(fidx, sense)]
                        form2idx[row["VALUE"], sense] = fidx

        with self.cldf_writer(args) as writer:
            # add sources
            writer.add_sources()
            # add languages for both
            for language in self.languages:
                writer.add_language(
                        ID=language["ID"],
                        Name=language["Name"],
                        Family=language["Family"],
                        Glottocode=language["Glottocode"],
                        )
            args.log.info("added languages")

            language_table = writer.cldf["LanguageTable"]

            # create CLDF set based on Swadesh-1955-100
            if RUN == "FULL":
                concepts = {}
                for concept in self.conceptlists[0].concepts.values():
                    # print(concept)
                    idx = concept.id.split("-")[-1] + "_" + slug(concept.concepticon_gloss)
                    writer.add_concept(
                        ID=idx,
                        Name=concept.english,
                        Concepticon_ID=concept.concepticon_id,
                        Concepticon_Gloss=concept.concepticon_gloss,
                    )
                    concepts[concept.concepticon_gloss] = idx

                new_index = 0
                for row in self.raw_dir.read_csv(
                        "raw_mapped.tsv", delimiter="\t", dicts=True
                        ):

                    if row["FORM"] != '':
                        new_index += 1
                        writer.add_forms_from_value(
                                ID=new_index,
                                Language_ID="Amahuaca",
                                Parameter_ID=concepts[row["CONCEPTICON_GLOSS"]],
                                Value=row["FORM"].strip(),
                                Meaning=row["MEANING"],
                                Entry_ID=form2idx[row["FORM"], row["SENSE"]],
                                Sense_ID=row["SENSE_ID"],
                                Source="Hyde1980"
                                )
            else:
                args.log.info("skipping concepts and VALUE")

        # Writing the dictionary
        with self.cldf_writer(args, cldf_spec="dictionary", clean=False) as writer:
            writer.cldf.add_component(language_table)

            # iterate over senses and values
            for sense, values in senses.items():
                for i, (fidx, sense_desc) in enumerate(values):
                    writer.objects["SenseTable"].append({
                        "ID": sense+"-"+str(i+1),
                        "Description": sense_desc,
                        "Entry_ID": fidx
                        })
            for fidx, row in idxs.items():
                writer.objects["EntryTable"].append({
                    "ID": fidx,
                    "Language_ID": "Amahuaca",
                    "Headword": row["VALUE"],
                    'Part_Of_Speech': row["POS"]
                    })
