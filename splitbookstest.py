from splitbooks import BookSplitter
import unittest

class TestBookSplitter(unittest.TestCase):

    def test_get_file_stem_simple(self):
        bs = BookSplitter()

        fs = bs.get_file_stem('ספר דברים/א')
        self.assertEqual(fs, 'ספר דברים')

    def test_get_file_stem_alefbet(self): # shmuel, malakhim, divrei hayamim
        bs = BookSplitter()

        fs = bs.get_file_stem('ספר דברי הימים/דה"א ג')
        # print(fs)
        self.assertEqual(fs, 'ספר דברי הימים - דה"א')

    def test_get_file_stem_minor(self): # trei asar, ezra/nehemiah
        bs = BookSplitter()

        fs = bs.get_file_stem('ספר תרי עשר/הושע א')
        # print(fs)
        self.assertEqual(fs, 'ספר תרי עשר - הושע')

    def test_get_file_stem_tehillim(self):
        bs = BookSplitter()

        # ספר ראשון 1-41
        fs = bs.get_file_stem('ספר תהלים/א')
        self.assertEqual(fs, 'ספר תהלים - ראשון')
        fs = bs.get_file_stem('ספר תהלים/מא')
        self.assertEqual(fs, 'ספר תהלים - ראשון')

        # ספר שני 42-72
        fs = bs.get_file_stem('ספר תהלים/מב')
        self.assertEqual(fs, 'ספר תהלים - שני')
        fs = bs.get_file_stem('ספר תהלים/עב')
        self.assertEqual(fs, 'ספר תהלים - שני')

        # ספר שלישי 73-89
        fs = bs.get_file_stem('ספר תהלים/עג')
        self.assertEqual(fs, 'ספר תהלים - שלישי')
        fs = bs.get_file_stem('ספר תהלים/פט')
        self.assertEqual(fs, 'ספר תהלים - שלישי')

        # זפר רביעי 90-106
        fs = bs.get_file_stem('ספר תהלים/צ')
        self.assertEqual(fs, 'ספר תהלים - רביעי')
        fs = bs.get_file_stem('ספר תהלים/קו')
        self.assertEqual(fs, 'ספר תהלים - רביעי')

        # ספר חמישי 107-150
        fs = bs.get_file_stem('ספר תהלים/קז')
        self.assertEqual(fs, 'ספר תהלים - חמישי')
        fs = bs.get_file_stem('ספר תהלים/קנ')
        self.assertEqual(fs, 'ספר תהלים - חמישי')

    def test_get_file_stem_bereshit(self):
        bs = BookSplitter()

        fs = bs.get_file_stem('ספר בראשית/א')
        self.assertEqual(fs, 'ספר בראשית - א-יא')

        fs = bs.get_file_stem('ספר בראשית/יא')
        self.assertEqual(fs, 'ספר בראשית - א-יא')

        fs = bs.get_file_stem('ספר בראשית/יב')
        self.assertEqual(fs, 'ספר בראשית - יב-נ')

        fs = bs.get_file_stem('ספר בראשית/נ')
        self.assertEqual(fs, 'ספר בראשית - יב-נ')

if __name__ == '__main__':
    unittest.main()