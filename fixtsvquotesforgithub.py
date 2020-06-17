import csv
import sys

filepath = sys.argv[1]

print(filepath)

with open(filepath, encoding='utf-8') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        rows = [row for row in tsvreader]

with open(filepath, 'w', newline='', encoding='utf-8') as outfile:
    tsvwriter = csv.writer(outfile, dialect='excel-tab')
    tsvwriter.writerows(rows)
