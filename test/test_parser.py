import unittest
import os
from src.parser.ticker_parser import clean_tickers, load_local_ticker


class TestTickerFunctions(unittest.TestCase):

    def setUp(self):
        self.file_path = 'test_data.csv'
        self.ticker_list = []

    def test_load_local_ticker_with_data(self):
        with open(self.file_path, 'w') as csvfile:
            csvfile.write('AAPL\nGOOGL\nMSFT\n')
        load_local_ticker(self.file_path, self.ticker_list)
        self.assertEqual(self.ticker_list, ['AAPL', 'GOOGL', 'MSFT'])

    def test_load_local_ticker_with_empty_file(self):
        load_local_ticker(self.file_path, self.ticker_list)
        self.assertEqual(self.ticker_list, [])

    def test_load_local_ticker_with_no_data(self):
        with open(self.file_path, 'w') as csvfile:
            csvfile.write('')
        load_local_ticker(self.file_path, self.ticker_list)
        self.assertEqual(self.ticker_list, [])

    def tearDown(self):
        if self.file_path in os.listdir():
            os.remove(self.file_path)

    def test_empty_list(self):
        empty_list = []
        cleaned_list = clean_tickers(empty_list)
        self.assertEqual(cleaned_list, [])

    def test_single_empty_string(self):
        test_list = ['']
        cleaned_list = clean_tickers(test_list)
        self.assertEqual(cleaned_list, [])

    def test_single_non_empty_string(self):
        test_list = ['abc']
        cleaned_list = clean_tickers(test_list)
        self.assertEqual(cleaned_list, ['abc'])

    def test_multiple_strings_with_leading_trailing_whitespaces(self):
        test_list = [' abc ', ' def  ']
        cleaned_list = clean_tickers(test_list)
        self.assertEqual(cleaned_list, ['abc', 'def'])

    def test_multiple_strings_with_leading_trailing_whitespaces_and_empty_strings(self):
        test_list = [' abc ', '', ' def  ', '']
        cleaned_list = clean_tickers(test_list)
        self.assertEqual(cleaned_list, ['abc', 'def'])


if __name__ == '__main__':
    unittest.main()
