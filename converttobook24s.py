import json
import os
import glob
import pprint

"""Older version of MAM-Data had books grouped into 6 files. This script converts those 6 files into 24 files, one for each book."""

directory = R"C:/Users/marc/code/miqra-data/miqra-json/"

# Get a list of all files whose file name begins with "MAM"
files = glob.glob(os.path.join(directory, "MAM*"))

print(files)

book24_names = []
book24_names_only = []

# Iterate over each file
for file in files:
    with open(file, encoding="utf-8") as input_file:
        # with open(output_file_path, "w", encoding="utf-8") as output_file:
        data = json.load(input_file)
        # Iterate over each book in the file
        for book in data["body"]:
            # Create a new file name for the book
            book24_name = book["book_name"]
            if book24_name not in book24_names_only:
                book24_names_only.append(book24_name)
                book24_names.append(
                    {
                        "book24_name": book24_name,
                        "mam_parsed_file_stem": "",
                        "mam_parsed_file_stem_old": os.path.splitext(
                            os.path.basename(file)
                        )[0],
                    }
                )

            # Create a new file path for the book
            # book_file_path = os.path.join(directory, book_file_name)
            # # Write the book to the new file
            # with open(book_file_path, "w", encoding="utf-8") as book_file:
            #     json.dump(book, book_file, ensure_ascii=False, indent=4)

pprint.pprint(book24_names, indent=4)
print(len(book24_names))

# Output book24_names to book24names.json
# with open("book24names.json", "w", encoding="utf-8") as output_file:
#     json.dump(book24_names, output_file, ensure_ascii=False, indent=4)
