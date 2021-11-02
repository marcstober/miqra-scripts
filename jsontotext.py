"""Turns MAM JSON into plain text HTML."""
import argparse
import io
import json

from pathlib import Path
from html import escape

arg_parser = argparse.ArgumentParser(description='Turns MAM JSON into plain text HTML.')
arg_parser.add_argument('input_file_path')
arg_parser.add_argument('--template-table', dest='template_table', default=False, action='store_true', help='show table of templates found')
args = arg_parser.parse_args()

# TODO: this strips things down to a plain text - create version that preserves special formatting, notes, etc.
# TODO: remove odd "HTML" tag in Deut. 11:21 - asked about fix upstream

class JsonToText:
    """Turns MAM JSON into plain text HTML."""

    def __init__(self):
        self.found_template_names = {}

    def dispatch_template(self, item):
        template_data = item['tmpl']
        template_name = template_data[0][0]

        if template_name in self.found_template_names:
            self.found_template_names[template_name]['count'] += 1
        else:
            self.found_template_names[template_name] = {'count': 1}

        if template_name == 'נוסח':
            return self.process_template_nusach(item)
        if template_name == 'מ:פסק':
            return self.process_template_psik()
        if template_name == 'מ:לגרמיה':
            return self.process_template_psik() # TODO: something different?
        if template_name == 'מ:קמץ':
            return self.process_template_kamatz(item)
        if template_name == 'מ:ששש':
            return self.process_template_setumah()
        if template_name == 'ר3':
            return self.process_template_setumah()
        if template_name == 'קו"כ-אם':
            return self.process_template_nusach(item)
        if template_name == 'מ:הערה':
            return ''
        if template_name == 'כו"ק':
            return self.process_template_ketiv_keri(item)
        if template_name == 'שני טעמים באות אחת':
            return self.process_template_two_tropes(item)
        if template_name == 'מ:אות מנוקדת':
            return self.process_template_nusach(item)
        if template_name == 'מ:אות-ג':
            return self.process_template_nusach(item)
        if template_name == 'מ:אות-ק':
            return self.process_template_nusach(item)
        if template_name == 'קו"כ':
            return self.process_template_ketiv_keri(item)
        if template_name == 'סס':
            return self.process_template_setumah()
        if template_name == 'ססס':
            return self.process_template_setumah()
        if template_name == 'מ:גרשיים ותלישא גדולה':
            return self.process_template_gershayim_telisha_gedolah()
        if template_name == 'מ:כו"ק כתיב מילה חדה וקרי תרתין מילין':
            return self.process_template_ketiv_keri(item)
        if template_name == 'פסקא באמצע פסוק':
            return self.process_template_setumah()
        if template_name == 'מ:נו"ן הפוכה':
            return self.process_template_nusach(item)
        if template_name == 'ירח בן יומו':
            return '\u05AA'

        self.found_template_names[template_name]['handled'] = False
        return self.process_template(item)

    def process_template_nusach(self, item):
        """Handles any case where the desired output is the first template parameter."""
        template_items = item['tmpl']
        # FUTURE: footnotes or similar?
        # return '<span style="color: green">{}</span>'.format(self.process_templates(template_items[1]))
        return self.process_templates(template_items[1])

    def process_template_psik(self):
        return ' \u05C0 ';

    def process_template_kamatz(self, item):
        template_items = item['tmpl']
        for template_item in [ti[0] for ti in template_items]:
            if template_item.startswith('ד='):
                return template_item.split('=')[1]
        raise "error" # TODO proper exception

    def process_template_setumah(self):
        return ' ';

    def process_template_ketiv_keri(self, item):
        template_items = item['tmpl']
        return '{} [{}]'.format(template_items[1][0], template_items[2][0])

    def process_template_two_tropes(self, item):
        template_items = item['tmpl']
        return '{}{}'.format(template_items[1][0], template_items[2][0])

    def process_template_gershayim_telisha_gedolah(self):
        return '\u05A0\u059E' # TODO: in Lev. 10:4, why not different mark on each character?

    def process_template(self, item):
        '''Default template handler.'''
        output_string = '<span style="color: red">TEMPLATE(</span>'
        # template is a list of lists, although second level is (always?) a 1-item list, unless a nested template
        is_first = True
        for template_item in item['tmpl']:
            if is_first:
                is_first = False
                # first item of template is template type
                # print('UNRESOLVED: {}'.format(template_item[0]))
                output_string += '<span style="color: #99f">{}</span>'.format(self.process_templates(template_item)) # TODO: really need to call process_templates here?
            else:
                output_string += '<span style="color: red">, </span>'
            # output_string += escape(str(template_item))
                output_string += self.process_templates(template_item)
        output_string += '<span style="color: red">)</span>'
        return output_string

    def process_templates(self, data):
        output_string = ''
        for item in data:
            if isinstance(item, str):
                if '//' in item:
                    item = item.replace('//', '')
                output_string += escape(item)
            else:
                if 'tmpl' in item:
                    output_string += self.dispatch_template(item)
                elif 'custom_tag' in item:
                    output_string += escape('<{}>'.format(item['custom_tag']))
        return output_string

    def main(self):
        input_file_path = Path(args.input_file_path).resolve()
        file_stem = input_file_path.stem
        output_file_path = input_file_path.parent.parent.joinpath('miqra-json-html').joinpath(file_stem).with_suffix('.html')
        print(output_file_path)

        temp_stream = io.StringIO()

        with open(args.input_file_path, encoding='utf-8') as input_file:
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                data = json.load(input_file)

                for book in data['body']:
                    temp_stream.write('\n<h1>{}</h1>'.format(escape(book['book_name'])))
                    if book['sub_book_name']:
                        temp_stream.write('<h1>: {}</h1>'.format(escape(book['sub_book_name'])))
                    chapters = book['chapters']
                    for hebrew_chapter_number in chapters:
                        temp_stream.write('\n<h2>פרק {}</h2>'.format(escape(hebrew_chapter_number)))
                        chapter = chapters[hebrew_chapter_number]
                        for hebrew_verse_number in chapter:
                            verse = chapter[hebrew_verse_number]
                            if len(verse) != 3: # validate that there are 3 "columns" (from the spreadsheet) in a verse
                                raise "error" # TODO exception
                            # TODO: The actual text is in the third item - do something with other info.
                            # process_templates(verse[0], temp_stream)
                            # process_templates(verse[1], temp_stream)
                            resolved_html = self.process_templates(verse[2])
                            if resolved_html:
                                temp_stream.write('\n<h3>{}</h3>'.format(escape(hebrew_verse_number)))
                                output_string = '\n<p>'
                                temp_stream.write(resolved_html)
                                output_string += '</p>'
                
                if args.template_table:
                    output_file.write('\n<table border="1">')
                    for key in self.found_template_names:
                        if 'handled' in self.found_template_names[key] and not self.found_template_names[key]['handled']:
                            output_file.write('\n<tr><td>{}</td><td style="color: red">{}</td></tr>'.format(escape(str(key)), escape(str(self.found_template_names[key]))))
                        else:
                            output_file.write('\n<tr><td>{}</td><td>{}</td></tr>'.format(escape(str(key)), escape(str(self.found_template_names[key]['count']))))
                    output_file.write('\n</table>')

                output_file.write('<div dir="rtl">')

                output_file.write(temp_stream.getvalue())

                output_file.write('</div>')

if __name__ == '__main__':
    JsonToText().main()
