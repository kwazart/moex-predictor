import unittest

from src.parser.price_parser import get_tickers
from src.parser.ticker_parser import clean_tickers


class TestTickerParser(unittest.TestCase):

    def setUp(self):
        self.ticker_path = "ticker-test.csv"

    def test_get_tickers_valid_path(self):
        """
        Test that get_tickers returns a list of cleaned tickers when given a valid path.
        """
        expected_tickers = ['AAA', 'BBB', 'CCC']
        actual_tickers = get_tickers(self.ticker_path)
        self.assertEqual(actual_tickers, expected_tickers)

    def test_get_tickers_invalid_path(self):
        """
        Test that get_tickers returns an empty list when given an invalid path.
        """
        invalid_path = 'invalid_path.csv'
        with self.assertRaises(FileNotFoundError):
            get_tickers(invalid_path)

    def test_clean_tickers_valid_input(self):
        """
        Test that clean_tickers returns a list of cleaned tickers when given a valid input.
        """
        expected_cleaned_tickers = ['SBER', 'GAZP', 'SBERPFD']
        actual_cleaned_tickers = clean_tickers(['SBER', 'GAZP', 'SBERPFD'])
        self.assertEqual(actual_cleaned_tickers, expected_cleaned_tickers)

    def test_clean_tickers_invalid_input(self):
        """
        Test that clean_tickers returns an empty list when given an invalid input.
        """
        invalid_input = ['invalid_ticker', '1234567890']
        actual_cleaned_tickers = clean_tickers(invalid_input)
        self.assertEqual(actual_cleaned_tickers, invalid_input)

    def test_clean_tickers_empty_input(self):
        """
        Test that clean_tickers returns an empty list when given an empty input.
        """
        empty_input = []
        actual_cleaned_tickers = clean_tickers(empty_input)
        self.assertEqual(actual_cleaned_tickers, [])
