import csv


def load_local_ticker(file_path, ticker_list):
    """
        Loads local ticker data from a CSV file into a list.

        Args:
        file_path (str): The path to the CSV file containing the ticker data.
        ticker_list (list): A list to store the loaded ticker data.

        Returns:
        None. The function modifies the ticker_list in-place.

        Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    with open(file_path, newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if len(row) > 0:
                ticker_list.append(row[0])


def clean_tickers(ticker_list):
    return list(map(lambda non_stripped_x: non_stripped_x.strip(),
                    list(filter(lambda x: x.strip() != '', ticker_list))))


def clear_tickers(ticker_list):
    ticker_list.clear()
