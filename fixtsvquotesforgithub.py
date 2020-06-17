import csv
import sys

# To show TSV files nicely, Github requires any cell that has a quotation mark in it to:
#   1. have the whole cell surrounded with quotation marks
#   2. have any question marks doubled
# The "excel-tab" dialect built into the Python csv module does this.

filepath = sys.argv[1]

print(filepath)

with open(filepath, encoding='utf-8') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        rows = [row for row in tsvreader]

with open(filepath, 'w', newline='', encoding='utf-8') as outfile:
    tsvwriter = csv.writer(outfile, dialect='excel-tab')
    tsvwriter.writerows(rows)
