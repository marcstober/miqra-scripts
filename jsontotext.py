import json

from html import escape

# TODO: add back in anything interesting from the other columns (aliyot, ptichah/stuma, etc.)
# TODO: actually resolve templates

def resolve_templates(data):
    output_string = ''
    for item in data:
        if isinstance(item, str):
            output_string += escape(item)
        else:
            if 'tmpl' in item:
                output_string += '<span style="color: red">TEMPLATE(</span>'
                # template is a list of lists, although second level is (always?) a 1-item list, unless a nested template
                is_first = True
                for template_item in item['tmpl']:
                    if is_first:
                        is_first = False
                        # first item of template is template type
                        output_string += '<span style="color: #99f">{}</span>'.format(resolve_templates(template_item)) # TODO: really need to call resolve_templates here?
                    else:
                        output_string += '<span style="color: red">, </span>'
                    # output_string += escape(str(template_item))
                        output_string += resolve_templates(template_item)
                output_string += '<span style="color: red">)</span>'
            elif 'custom_tag' in item:
                output_string += escape('<{}>'.format(item['custom_tag']))
    return output_string

def main():
    with open(r'..\miqra-data\miqra-json\MAM-Torah.json', encoding='utf-8') as input_file:
        with open(r'..\miqra-data\miqra-json\MAM-Torah.html', 'w', encoding='utf-8') as output_file:
            data = json.load(input_file)

            # for item in data['header']:
            #     output_file.write(escape(item))

            output_file.write('<div dir="rtl">')

            for book in data['body']:
                output_file.write('<h1>{}</h1>'.format(escape(book['book_name'])))
                if book['sub_book_name']:
                    output_file.write('<h1>: {}</h1>'.format(escape(book['sub_book_name'])))
                chapters = book['chapters']
                for hebrew_chapter_number in chapters:
                    output_file.write('<h2>פרק {}</h2>'.format(escape(hebrew_chapter_number)))
                    chapter = chapters[hebrew_chapter_number]
                    for hebrew_verse_number in chapter:
                        output_file.write('<h3>{}</h3>'.format(escape(hebrew_verse_number)))
                        verse = chapter[hebrew_verse_number]
                        if len(verse) != 3: # validate that there are 3 "columns" (from the spreadsheet) in a verse
                            raise "error" # TODO exception
                        # TODO: The actual text is in the third item - do something with other info.
                        # resolve_templates(verse[0], output_file)
                        # resolve_templates(verse[1], output_file)
                        output_string = '\n<p>'
                        output_file.write(resolve_templates(verse[2]))
                        output_string += '</p>'

if __name__ == '__main__':
    main()
