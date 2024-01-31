"""This module parses the Amahuaca dictionary into a csv-file."""
import csv
import re
from collections import defaultdict

entries = defaultdict()
pos = ['(n.)', '(vt.)', '(vi.)', '(adv.)', '(adj.)', '(nf.)', '(conj.)', '(pn.)', '(vr.)',
       '(int.)', '(n.):', '(vt.):', '(vi.):', '(adv.):', '(adj.):', '(nm.):', '(nf.):', '(conj.):',
       '(pn.):', '(vr.):', '(rm.):', '(nm.).', ':', '(nm.)', '(nma.)']


def split_string_on_pos(string, delim):
    """Splits input string on any delim of pos-list."""
    pattern = '|'.join(map(re.escape, delim))
    out = re.split(f'({pattern})', string)
    out = [item for item in out if item]

    return out


with open("hyde_esp.txt", "r", encoding="utf8") as f:
    i = 0

    for line in f.readlines():
        if line not in ['\n', '']:
            # Special condition for ill-formated entries
            if 'coragyps' in line:
                IDX = i - 1
                line = line.split('. ')
                entries[IDX] = entries[IDX] + line[0]
                entries[i] = line[1]
                entries[i] = entries[i].replace('¬\n', '')
            elif '\tnáhin, pózun' in line:
                IDX = i - 1
                entries[IDX] = 'tocar (vi.) távu-távuhí,'
                entries[i] = 'tocar (vt.) rámanquín, vúaquín.'
            elif 'rámanquín, vúaquín.' in line:
                IDX = i - 1
                entries[IDX] = 'perezoso (adj.) yonotíma.'
                entries[i] = 'perezoso (nm.) náhin, pózun.'
            # General condition
            elif any(item in line for item in pos):
                entries[i] = line
            else:
                IDX = i - 1
                entries[i] = entries[IDX] + line
                entries[i] = entries[i].replace('¬\n', '')
                del entries[IDX]
            i += 1


output = [['GLOSS', 'POS', 'VALUE']]
# Splitting the entries
for i, item in enumerate(entries):
    entry = entries[item].replace('\n', '')
    entry = entry.replace('\t', ' ')

    entry = split_string_on_pos(entry, pos)

    key = entry[0].strip()
    sep = entry[1].replace(':', '') if entry[1] != ':' else ''
    forms = entry[2] if entry[2] != ':' else entry[3]
    forms = forms.replace('.', '')
    forms = forms.strip()
    forms = forms.split(', ')

    for form in forms:
        output.append([key, sep, form])

with open('../parsed_raw.tsv', 'w', encoding="utf8") as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerows(output)
