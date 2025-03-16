import unittest

from src.util.convert_alphabet_index import convert_alphabet_index


class TestConvertAlphabetIndex(unittest.TestCase):
    def test_convert_alphabet_index_non_word_input(self):
        with self.assertRaises(ValueError):
            convert_alphabet_index('word')

    def test_convert_alphabet_index_numeric_string_input(self):
        with self.assertRaises(ValueError):
            convert_alphabet_index('5')

    def test_convert_alphabet_index_numeric_input(self):
        with self.assertRaises(ValueError):
            convert_alphabet_index(1)

    def test_convert_alphabet_index_non_alphabet_str_input(self):
        with self.assertRaises(ValueError):
            convert_alphabet_index("*")

    def test_convert_alphabet_index_lower_case_letter_input(self):
        results = convert_alphabet_index("a")
        self.assertEqual(0, results)

    def test_convert_alphabet_index_upper_case_letter_input(self):
        results = convert_alphabet_index("A")
        self.assertEqual(0, results)


if __name__ == '__main__':
    unittest.main()
