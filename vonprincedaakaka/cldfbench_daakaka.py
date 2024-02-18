from collections import ChainMap 
import pathlib
import re
import attr
import pylexibank
from pylexibank import Lexeme
from pylexibank import Dataset as BaseDataset
from cldfbench import CLDFSpec
from clldutils.misc import slug

from pydictionaria.sfm_lib import Database as SFM, Entry
from pydictionaria import sfm2cldf


PC_PATTERN = re.compile(r'illustrations/(?P<stem>[^\.]+)\.txt')
GE_PATTERN = re.compile(r'\$(?P<term>[a-z1-3][a-z]*)')

# RUN = 'PRE'
RUN = 'FULL'


@attr.s
class CustomLexeme(Lexeme):
    Meaning = attr.ib(default=None)
    Sense_ID = attr.ib(default=None)
    Entry_ID = attr.ib(default=None)


def preprocess(entry):
    new = Entry()
    has_de = bool(entry.get('de'))
    if entry.get('dnp'):
        pass
    for i, (marker, content) in enumerate(entry):
        if marker == 'sn':
            has_de = False
        if marker == 'pc':
            content = PC_PATTERN.sub(lambda m: m.group('stem') + '.png', content)
        if marker == 'ge' and not has_de:
            new.append(('de', content))
        #    content = GE_PATTERN.sub(lambda m: m.group('term').upper(), content)
        new.append((marker, content))

    return new


def authors_string(authors):
    def is_primary(a):
        return not isinstance(a, dict) or a.get('primary', True)

    primary = ' and '.join(
        a['name'] if isinstance(a, dict) else a
        for a in authors
        if is_primary(a))
    secondary = ' and '.join(
        a['name']
        for a in authors
        if not is_primary(a))
    if primary and secondary:
        return '{} with {}'.format(primary, secondary)
    else:
        return primary or secondary


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "daakaka"
    lexeme_class = CustomLexeme

    def cldf_specs(self):
        return {
            None: pylexibank.Dataset.cldf_specs(self),
            "dictionary": CLDFSpec(
                module="Dictionary",
                dir=self.cldf_dir,
            ),
        }

    def cmd_download(self, args):
        """
        Download files to the raw/ directory. You can use helpers methods of `self.raw_dir`, e.g.

        >>> self.raw_dir.download(url, fname)
        """
        pass

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.

        >>> writer.objects['LanguageTable'].append(...)
        """

        # read data
        with self.cldf_writer(args, cldf_spec='dictionary') as writer:
            md = self.etc_dir.read_json('md.json')
            properties = md.get('properties') or {}
            language_name = md['language']['name']
            isocode = md['language']['isocode']
            language_id = next(
                row
                for row in self.etc_dir.read_csv('languages.csv', dicts=True)
                if row['Glottocode'] == 'daka1243')['ID']
            glottocode = md['language']['glottocode']

            marker_map = ChainMap(
                properties.get('marker_map') or {},
                sfm2cldf.DEFAULT_MARKER_MAP)
            entry_sep = properties.get('entry_sep') or sfm2cldf.DEFAULT_ENTRY_SEP
            sfm = SFM(
                self.raw_dir / 'db.sfm',
                marker_map=marker_map,
                entry_sep=entry_sep)

            examples = sfm2cldf.load_examples(self.raw_dir / 'examples.sfm')

            if (self.etc_dir / 'cdstar.json').exists():
                media_catalog = self.etc_dir.read_json('cdstar.json')
            else:
                media_catalog = {}

            # preprocessing

            sfm.visit(preprocess)

            # processing

            with open(self.dir / 'cldf.log', 'w', encoding='utf-8') as log_file:
                log_name = '%s.cldf' % language_id
                cldf_log = sfm2cldf.make_log(log_name, log_file)

                entries, senses, examples, media = sfm2cldf.process_dataset(
                    self.id, language_id, properties,
                    sfm, examples, media_catalog=media_catalog,
                    glosses_path=self.raw_dir / 'glosses.flextext',
                    examples_log_path=self.dir / 'examples.log',
                    glosses_log_path=self.dir / 'glosses.log',
                    cldf_log=cldf_log)

                # postprocess

                for item in media:
                    item['Description'] = 'Copyright by Tio Bang'

                # cldf schema

                sfm2cldf.make_cldf_schema(
                    writer.cldf, properties,
                    entries, senses, examples, media)
                # Ensure the dictionary knows about the columns lexibank will
                # make when it overwrites the language table.
                writer.cldf.add_columns(
                    'LanguageTable', 'Glottolog_Name', 'Family')

                sfm2cldf.attach_column_titles(writer.cldf, properties)

                print(file=log_file)

                entries = sfm2cldf.ensure_required_columns(
                    writer.cldf, 'EntryTable', entries, cldf_log)
                senses = sfm2cldf.ensure_required_columns(
                    writer.cldf, 'SenseTable', senses, cldf_log)
                examples = sfm2cldf.ensure_required_columns(
                    writer.cldf, 'ExampleTable', examples, cldf_log)
                media = sfm2cldf.ensure_required_columns(
                    writer.cldf, 'media.csv', media, cldf_log)

                entries = sfm2cldf.remove_senseless_entries(
                    senses, entries, cldf_log)

            # output

            writer.cldf.properties['dc:creator'] = authors_string(
                md.get('authors') or ())

            writer.objects['EntryTable'] = entries
            writer.objects['SenseTable'] = senses
            writer.objects['ExampleTable'] = examples
            writer.objects['media.csv'] = media

            with self.cldf_writer(args, clean=False) as writer:
                writer.add_sources()
                # add languages for both
                for language in self.languages:
                    writer.add_language(
                        ID=language["ID"],
                        Name=language["Name"],
                        Family=language["Family"],
                        Glottocode=language["Glottocode"])

                args.log.info("added languages")

                concepts = {}
                for concept in self.conceptlists[0].concepts.values():
                    # print(concept)
                    idx = '{}_{}'.format(
                        concept.id.split("-")[-1],
                        slug(concept.concepticon_gloss))
                    writer.add_concept(
                        ID=idx,
                        Name=concept.english,
                        Concepticon_ID=concept.concepticon_id,
                        Concepticon_Gloss=concept.concepticon_gloss)
                    concepts[concept.concepticon_gloss] = idx

                if RUN == "FULL":
                    new_index = 0
                    mapped_rows = self.raw_dir.read_csv(
                        "raw_filtermap.tsv", delimiter="\t", dicts=True)
                    for row in mapped_rows:
                        if row["FORM"] != '':
                            new_index += 1
                            writer.add_forms_from_value(
                                ID=new_index,
                                Parameter_ID=concepts[row["CONCEPTICON_GLOSS"]],
                                Value=row["FORM"],
                                Meaning=row["MEANING"],
                                Sense_ID=row["SENSE_ID"],
                                Language_ID="Daakaka",
                                Source="vonPrince2017")
