import csv
from hebrew_numbers import gematria_to_int
from pathlib import Path
import sys
import zipfile

class BookSplitter:
    def __init__(self):
        self.outdirpath = Path(r'C:\Users\Marc\code\miqra-data\source')
        self.output_rows = 0

    def split_books(self, filepath):

        self._path_obj = Path(filepath) 

        print(filepath)

        book = ''
        book_rows = []

        with open(filepath, encoding='utf-8') as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter='\t')
            for row_num, row in enumerate(tsvreader):
                # print(row[1])
                if(str(row[1]) == '0'):
                    new_book = self.get_file_stem(row[0])
                    if new_book != book:
                        if book:
                            self.save_book_rows(book, book_rows)
                        book = new_book
                        book_rows = []
                book_rows.append(row)
            
            self.save_book_rows(book, book_rows)

        # verify and cleanup
        input_rows = row_num + 1
        print('')
        print(' Input Rows: {}'.format(input_rows))
        print('Output Rows: {}'.format(self.output_rows))
        if input_rows != self.output_rows:
            raise Exception('input rows does not equal output rows')

    def get_file_stem(self, s):
        sefer, perek = s.split('/')
        if sefer == 'ספר בראשית':
            if gematria_to_int(perek) < 12:
                return 'ספר בראשית - א-יא'
            else:
                return 'ספר בראשית - יב-נ'
        elif sefer == 'ספר תהלים':
            if gematria_to_int(perek) < 42:
                return 'ספר תהלים - ראשון'
            elif gematria_to_int(perek) < 73:
                return 'ספר תהלים - שני'
            elif gematria_to_int(perek) < 90:
                return 'ספר תהלים - שלישי'
            elif gematria_to_int(perek) < 107:
                return 'ספר תהלים - רביעי'
            else:
                return 'ספר תהלים - חמישי'
        elif ' ' in perek:
            section = perek.split(' ')[0]
            # replace quotes, which can make a filename invalid, with proper gershayim
            section = section.replace('"', chr(0x05f4))
            return '{} - {}'.format(sefer, section)
        else:
            return sefer

    def save_book_rows(self, book, rows):

        print('Saving {} rows...'.format(len(rows)))

        dirpath = Path(self.outdirpath, self._path_obj.stem)
        if book:
            dirpath.mkdir(exist_ok=True) 
                
        filepath = Path(dirpath, book).with_suffix('.tsv')

        print('Saving to {}...'.format(filepath))

        with open(filepath, 'w', newline='', encoding='utf-8', ) as outfile:

            # To show TSV files nicely, Github requires any cell that has a quotation mark in it to:
            #   1. have the whole cell surrounded with quotation marks
            #   2. have any question marks doubled
            # The "excel-tab" dialect built into the Python csv module does this.

            tsvwriter = csv.writer(outfile, dialect='excel-tab')
            tsvwriter.writerows(rows)

        self.output_rows += len(rows)

if __name__ == '__main__':
    # BookSplitter().split_books(sys.argv[1])
    filenames = [
            'חמש מגילות.tsv', 
            'כתובים אחרונים.tsv', 
            'נביאים אחרונים.tsv', 
            'נביאים ראשונים.tsv',
            'ספרי אמת.tsv',
            'תורה.tsv',
            'README.tsv',
            'templates תבניות.tsv'
        ]
    dirname = r'C:\Users\marc\code\miqra-scripts\downloads'
    for filename in filenames:
        BookSplitter().split_books(Path(dirname, filename))

    with zipfile.ZipFile(Path(dirname, 'Miqra_al_pi_ha-Masorah.zip'), 'r') as zip_ref:
        zip_ref.extractall(Path(dirname, 'Miqra_al_pi_ha-Masorah'))

    import shutil
    shutil.copyfile(Path(dirname, 'Miqra_al_pi_ha-Masorah', 'README.tsv'), Path(r'C:\Users\Marc\code\miqra-data\source\README.tsv'))
    shutil.copyfile(Path(dirname, 'Miqra_al_pi_ha-Masorah', 'templates תבניות.tsv'), Path(r'C:\Users\Marc\code\miqra-data\source\templates תבניות.tsv'))
