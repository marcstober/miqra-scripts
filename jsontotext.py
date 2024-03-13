"""Convert provided MAM JSON file into a simple JSON file and an HTML file
    in which each verse is plain Unicode text."""

import argparse
import inspect
import io
import json
import os
from html import escape
from pathlib import Path
import pprint

arg_parser = argparse.ArgumentParser(description=__doc__)
arg_parser.add_argument("input_file_path")
arg_parser.add_argument(
    "--template-table",
    dest="template_table",
    default=False,
    action="store_true",
    help="show table of templates found",
)
args = arg_parser.parse_args()

# NOTE: This strips things down to a plain text. TODO: Create version that preserves special formatting, notes, etc.
# TODO: remove odd "HTML" tag in Deut. 11:21 - asked about fix upstream
# TODO: Handle all templates in the Tanakh (currently only handles those in Torah).
# TODO: Can this process be replaced by the simplified version for Sefaria that Ben has now in Github?


class JsonToText:
    """Turns MAM JSON into plain text HTML."""

    def __init__(self):
        self.found_templates = {}

    def dispatch_template(self, item):
        # template_data = item["tmpl"]
        template_name = item["tmpl_name"]

        if template_name in self.found_templates:
            self.found_templates[template_name]["count"] += 1
        else:
            self.found_templates[template_name] = {"count": 1}

        if template_name == "נוסח":
            # Handle the "documentation template".
            return self.process_template_nusach(item)
        if template_name == "מ:פסק":
            return self.process_template_psik()
        if template_name == "מ:לגרמיה-2":
            # TODO: ask Ben why MAM-parsed "plus version" has the "-2"
            # Currently has the same result as psik except for one less space.
            # A more advanced formatting application (beyond plain Unicode text) might handle it differently.
            return self.process_template_legarmeih()  # TODO: something different?
        if template_name == "מ:קמץ":
            return self.process_template_kamatz(item)
        if template_name == "מ:ששש":
            return self.process_template_setumah()
        if template_name == "ר3":
            return self.process_template_setumah()
        if template_name == 'קו"כ-אם':
            return self.process_template_nusach(item)
        if template_name == "מ:הערה":
            # TODO: still need this if "plus" version has "-2"?
            # Footnotes are not included in the output.
            # A more advanced formatting application might include them.
            return ""
        if template_name == "מ:הערה-2":
            # TODO: ask Ben why MAM-parsed "plus version" has the "-2"
            # it seems to be a different format in that the text being "footnoted" is inside the template
            return self.process_template_nusach(item)
        if template_name == 'כו"ק':
            return self.process_template_ketiv_keri(item)
        if template_name == "שני טעמים באות אחת":
            return self.process_template_two_tropes(item)
        if template_name == "שני טעמים באות אחת קמץ-תחתון-פתח-עליון":
            return self.process_template_qupo(item)
        if template_name == "מ:כפול":
            return self.process_template_kaful(item)
        if template_name == "מ:אות מנוקדת":
            return self.process_template_nusach(item)
        if template_name == "מ:אות-ג":
            return self.process_template_nusach(item)
        if template_name == "מ:אות-ק":
            return self.process_template_nusach(item)
        if template_name == 'קו"כ':
            # Handle "keri ketiv" like "ketiv keri".
            # On the related Wikisource project, "keri ketiv" is a way of formatting "ketiv keri" pairs that involve a maqef.
            # This application handles both cases the same way.
            return self.process_template_ketiv_keri(item)
        if template_name == "סס":
            return self.process_template_setumah()
        if template_name == "ססס":
            return self.process_template_setumah()
        if template_name == "מ:גרשיים ותלישא גדולה":
            return self.process_template_gershayim_telisha_gedolah()
        if template_name == 'מ:כו"ק כתיב מילה חדה וקרי תרתין מילין':
            return self.process_template_ketiv_keri(item)
        if template_name == 'מ:כו"ק כתיב תרתין מילין וקרי מילה חדה':
            return self.process_template_ketiv_keri(item)
        if template_name == "קרי ולא כתיב":
            return self.process_template_nusach(item)
        if template_name == "כתיב ולא קרי":
            return self.process_template_nusach(item)
        # it seems like instead of the "פסקא באמצע פסוק" template that used
        # to be in the source JSON, there's now just a "פפ" inside a verse
        if template_name == "פפ":
            return self.process_template_setumah()
        # if template_name == "פסקא באמצע פסוק":
        #     return self.process_template_setumah()
        if template_name == 'מ:נו"ן הפוכה':
            return self.process_template_nusach(item)
        if template_name == "ירח בן יומו":
            return "\u05AA"
        if template_name == "מ:טעם":
            return self.process_template_taam(item)
        if template_name == "מ:אות-מיוחדת-במילה":
            return self.process_template_special_letter(item)

        self.found_templates[template_name]["handled"] = False
        return self.process_template(item)

    def process_template_nusach(self, item):
        """Handle documentation template, or any other case where desired output is first template parameter."""
        template_items = item["tmpl_args"]
        template_items.insert(0, item["tmpl_name"])
        if self.current_verse == "לב:ו":
            print("AAA")
            print(template_items)
        template_items = [[ti] for ti in template_items]  # weird legacy format
        # FUTURE: footnotes or similar?
        # return '<span style="color: green">{}</span>'.format(self.process_templates(template_items[1]))
        if self.current_verse == "לב:ו":
            print("BBB")
            print(template_items[1])
        return self.process_templates(template_items[1])

    def process_template_psik(self):
        return " \u05C0 "

    def process_template_legarmeih(self):
        return " \u05C0"

    def process_template_kamatz(self, item):
        # print(item)  # debugging
        template_items = item["tmpl_args"] if "tmpl_args" in item else []
        template_items.insert(0, item["tmpl_name"])
        template_items = [[ti] for ti in template_items]  # weird legacy format
        # print(template_items)  # debugging
        for template_item in [ti[0] for ti in template_items]:
            if template_item.startswith("ד="):
                return template_item.split("=")[1]
        raise NotImplementedError

    def process_template_setumah(self):
        return " "

    def process_template_ketiv_keri(self, item):
        template_items = item["tmpl_args"] if "tmpl_args" in item else []
        template_items.insert(0, item["tmpl_name"])
        template_items = [[ti] for ti in template_items]  # weird legacy format
        return "{} [{}]".format(
            template_items[1][0], self.process_templates(template_items[2])
        )

    def process_template_two_tropes(self, item):
        template_items = item["tmpl"]
        return "{}{}".format(template_items[1][0], template_items[2][0])

    def process_template_qupo(self, item):
        template_items = item["tmpl"]
        # 034F = COMBINING GRAPHEME JOINER
        # 05B7 = HEBREW POINT PATAH
        return "\u034F\u05B7" + self.process_templates(template_items[1])

    def process_template_taam(self, item):
        # this is a weird one, you throw away 1st character and return second
        template_items = item["tmpl"]
        return template_items[1][0][1]

    def process_template_gershayim_telisha_gedolah(self):
        return "\u05A0\u059E"  # TODO: in Lev. 10:4, why not different mark on each character?

    def process_template_kaful(self, item):
        # print(self.current_verse)  # debugging
        # pprint.pprint(item)  # debugging
        template_items = item["tmpl_args"]

        # The first argument seems to be either a string beginning with "כפול" or a list of items,
        # the first one which is a string beginning with "כפול", but which then needs recursive processing.
        if isinstance(template_items[0], str):
            return template_items[0].replace("כפול=", "")

        template_items[0][0] = template_items[0][0].replace("כפול=", "")
        return self.process_templates(template_items[0])

    def process_template_special_letter(self, item):
        return self.process_templates([item["tmpl_args"][0]])

    def process_template(self, item):
        """Default template handler."""
        output_string = '<span style="color: red">TEMPLATE(</span>'
        # template is a list of lists, although second level is (always?) a 1-item list, unless a nested template
        is_first = True
        # print(item)  # debugging
        template_items = item["tmpl_args"] if "tmpl_args" in item else []
        template_items.insert(0, item["tmpl_name"])
        template_items = [[ti] for ti in template_items]  # weird legacy format
        for template_item in template_items:
            if is_first:
                is_first = False
                # first item of template is template type
                output_string += '<span style="color: #99f">{}</span>'.format(
                    self.process_templates(template_item)
                )  # TODO: really need to call process_templates here?
            else:
                output_string += '<span style="color: red">, </span>'
                # output_string += escape(str(template_item))
                output_string += self.process_templates(template_item)
        output_string += '<span style="color: red">)</span>'
        return output_string

    def process_templates(self, data):
        if not isinstance(data, list):
            raise ValueError("data must be a list")
        output_string = ""
        for item in data:
            # it's a string, a template, or a list that contains strings and/or templates
            if isinstance(item, list):
                output_string += self.process_templates(item)
            elif isinstance(item, str):
                if "//" in item:
                    # TODO: is this in current version of source JSON?
                    item = item.replace("//", "")
                # if self.current_verse == "ד:ה":
                #     print("  OH NO!")
                #     # print("data: ", data)
                #     print("SSS")
                #     print(item)
                #     if "tmpl" in item:
                #         print("very bad!")
                output_string += escape(item)
            else:
                # if it looks like a template
                if isinstance(item, dict) and "tmpl_name" in item:
                    s = self.dispatch_template(item)
                    if "tmpl" in s:
                        print("very bad!!")
                        print("---")
                        print(item)
                        print("---")
                        print(s)
                        print("---")
                        print("caller name:", inspect.stack()[1][3])
                        print("---")
                        print("---")
                    output_string += s
                elif "custom_tag" in item:
                    # TODO: is this in current version of source JSON?
                    # I'm not even sure we were handling it correctly before because the live parsh.io
                    # site had some escaped tags (e.g., "&lt;...&gt;")
                    output_string += escape("<{}>".format(item["custom_tag"]))

        # remove varika
        # TODO: put this back in once everything else is working and we know what it is (sheva na?)
        # output_string = output_string.replace("\u05B0", "")  # HEBREW POINT SHEVA
        output_string = output_string.replace("\uFB1E", "")

        if self.current_verse == "לב:ו":
            print("CCC")
            print(output_string)

        return output_string

    def main(self):
        input_file_path = Path(args.input_file_path).resolve()
        file_stem = input_file_path.stem

        with open(
            input_file_path.parent.parent.joinpath("book24names.json"), encoding="utf-8"
        ) as input_file:
            book24_names = json.load(input_file)

        # output_file_stem = None
        book24_names.sort(key=lambda book24: book24["number"])
        for book24_name in book24_names:
            if book24_name["mam_parsed_file_stem"] == file_stem:
                output_file_stem = book24_name["mam_parsed_file_stem_old"]
                this_book_number = book24_name["number"]
                break

        books_in_file = [
            book24_names["book24_name"]
            for book24_names in book24_names
            if book24_names["mam_parsed_file_stem_old"] == output_file_stem
        ]

        book24_names_by_hebrew_name = {}
        for book24_name in book24_names:
            book24_names_by_hebrew_name[book24_name["book24_name"]] = book24_name

        output_file_path = (
            input_file_path.parent.parent.joinpath("miqra-json-html")
            .joinpath(output_file_stem)
            .with_suffix(".html")
        )
        output_json_file_path = (
            input_file_path.parent.parent.joinpath("miqra-json-simple")
            .joinpath(output_file_stem)
            .with_suffix(".json")
        )
        print(output_file_path)

        simple_books = []

        temp_stream = io.StringIO()

        # vc = 0  # debugging

        with open(args.input_file_path, encoding="utf-8") as input_file:
            data = json.load(input_file)

            # In the source JSON, "book24" is the tradtional division of books (there are 24, some have sub-books),
            # and "book39s" is each sub-book separately (there are 39).
            # TODO: 5 sections of Psalms are not sub-books? (are they indicated in source JSON?)

            for book in data["book39s"]:
                simple_book = {}
                simple_books.append(simple_book)
                book_name = book["book24_name"]
                simple_book["book_name"] = book_name
                simple_book["sub_book_name"] = book["sub_book_name"]
                simple_book["chapters"] = {}

                temp_stream.write("\n<h1>{}</h1>".format(escape(book_name)))
                if book["sub_book_name"]:
                    temp_stream.write(
                        "<h1>: {}</h1>".format(escape(book["sub_book_name"]))
                    )
                chapters = book["chapters"]
                for hebrew_chapter_number in chapters:
                    simple_book["chapters"][hebrew_chapter_number] = {}

                    temp_stream.write(
                        "\n<h2>פרק {}</h2>".format(escape(hebrew_chapter_number))
                    )
                    chapter = chapters[hebrew_chapter_number]
                    for hebrew_verse_number in chapter:
                        verse = chapter[hebrew_verse_number]
                        self.current_verse = "{}:{}".format(
                            hebrew_chapter_number, hebrew_verse_number
                        )
                        if (
                            len(verse) != 3
                        ):  # validate that there are 3 "columns" (from the spreadsheet) in a verse
                            raise "error"  # TODO exception
                        # TODO: The actual text is in the third item - do something with other info.
                        # process_templates(verse[0], temp_stream)
                        # process_templates(verse[1], temp_stream)
                        template_items = verse[2]
                        # if (
                        #     hebrew_chapter_number == "א" and hebrew_verse_number == "ב"
                        # ):  # debugging
                        #     print(book_name, template_items)
                        # vc += 1
                        # if vc > 10:
                        #     continue
                        resolved_html = self.process_templates(template_items)
                        if resolved_html:
                            simple_book["chapters"][hebrew_chapter_number][
                                hebrew_verse_number
                            ] = resolved_html

                            temp_stream.write(
                                "\n<h3>{}</h3>".format(escape(hebrew_verse_number))
                            )
                            # output_string = "\n<p>"
                            temp_stream.write(resolved_html)
                            # output_string += "</p>"

            # TODO: Is this working?
            if args.template_table:
                self.write_template_table(temp_stream)

            # load the output files if they already exist
            # html
            existing_output_data = []
            if os.path.exists(output_file_path):
                with open(
                    output_file_path, "r", encoding="utf-8"
                ) as existing_output_file:
                    existing_output_data = existing_output_file.readlines()
            # json
            existing_simple_books = []
            if os.path.exists(output_json_file_path):
                with open(
                    output_json_file_path, "r", encoding="utf-8"
                ) as existing_json_file:
                    existing_simple_books = json.load(existing_json_file)

            existing_simple_books_by_name = {}
            for existing_simple_book in existing_simple_books:
                existing_simple_books_by_name[existing_simple_book["book_name"]] = (
                    existing_simple_book
                )

            # splice in this book
            # new_simple_books = []
            # for book in books_in_file:
            #     if book in existing_simple_books_by_name:
            #         new_simple_books.append(existing_simple_books_by_name[book])
            #     elif book ==

            existing_simple_books.extend(simple_books)

            def get_book_number(book_name):
                return book24_names_by_hebrew_name[book_name]["number"]

            existing_simple_books.sort(
                key=lambda book: get_book_number(book["book_name"])
            )

            simple_books = existing_simple_books

            existing_books = {}
            current_book = []

            for line in existing_output_data:
                if line.startswith("<h1>"):
                    hebrew_book_name = line.split("<h1>")[1].split("</h1>")[0]
                    book_number = book24_names_by_hebrew_name[hebrew_book_name].get(
                        "number", 0
                    )
                    # print(
                    #     "existing book: {} {}".format(hebrew_book_name, book_number)
                    # )  # debugging
                    current_book = []
                    existing_books[book_number] = current_book
                if len(existing_books):
                    current_book.append(line)

            # splice in this book

            existing_books[this_book_number] = temp_stream.getvalue().split("\n")

            # write the output file
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write("<!DOCTYPE html>\n")
                output_file.write('<div dir="rtl">')

                print("existing books: {}".format(existing_books.keys()))

                for existing_book_key in sorted(existing_books.keys()):
                    existing_book = existing_books[existing_book_key]
                    for line in existing_book:
                        if line.strip():
                            output_file.write("\n" + line.strip())

                if not line.endswith("</div>"):
                    output_file.write("</div>")
            print('HTML written to "{}".'.format(output_file_path))

            with open(output_json_file_path, "w", encoding="utf-8") as output_json_file:
                json.dump(simple_books, output_json_file, indent=2, ensure_ascii=False)
            print('JSON written to "{}".'.format(output_json_file_path))

    def write_template_table(self, output_file):
        output_file.write('\n<table border="1">')
        for key in self.found_templates:
            if (
                "handled" in self.found_templates[key]
                and not self.found_templates[key]["handled"]
            ):
                output_file.write(
                    '\n<tr><td>{}</td><td style="color: red">{}</td></tr>'.format(
                        escape(str(key)),
                        escape(str(self.found_templates[key])),
                    )
                )
            else:
                output_file.write(
                    "\n<tr><td>{}</td><td>{}</td></tr>".format(
                        escape(str(key)),
                        escape(str(self.found_templates[key]["count"])),
                    )
                )
        output_file.write("\n</table>\n")


if __name__ == "__main__":
    JsonToText().main()
