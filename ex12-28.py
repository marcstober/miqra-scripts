import unicodedata


def debug_string(s):
    # print(f"*** {desc} ***")
    for c in s:
        print(c, ord(c), unicodedata.name(c))


debug_string("וַֽיַּעֲשׂ֖וּ")

print("-" * 10)

debug_string("תׇֽעׇבְדֵ֔ם")
