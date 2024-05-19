import os

import pandas as pd
import requests
import apimoex
from datetime import datetime, timedelta
from pathlib import Path

from src.parser.ticker_parser import load_local_ticker, clean_tickers

ROOT = Path(__file__).parent.parent.parent
ticker_file_path = 'ticker.csv'
main_data_path = 'data.csv'
data_path = "data"
ticker_n = 'SBER' # тикер взятый за эталон


def get_tickers(ticker_path = os.path.join(ROOT, data_path, ticker_file_path)):
    """
    Получение списка тикеров из файла
    :param ticker_path: путь к файлу с тикерами
    :return: список тикеров
    """
    ticker_list = []
    load_local_ticker(ticker_path, ticker_list)
    return clean_tickers(ticker_list)


def get_data_by_date(start_date, end_date, ticker_name):
    """
    Получение данных по тикеру за определенный период времени
    :param start_date: дата начала периода
    :param end_date: дата конца периода
    :param ticker_name: тикер
    :return: DataFrame с данными
    """
    with requests.Session() as session:
        data = apimoex.get_board_history(session, ticker_name, start=start_date, end=end_date)
        df = pd.DataFrame(data)
        if len(df) == 0:
            return None
        df['price'] = df.VALUE / df.VOLUME
        df['TRADEDATE'] = pd.to_datetime(df['TRADEDATE'])
        return df[['TRADEDATE', 'price']].groupby(pd.Grouper(key='TRADEDATE', freq='M')).mean().reset_index()


def get_start_and_end_dates(year_ago):
    """
    Получение дат начала и конца периода
    :param year_ago: количество лет назад
    :return: дата начала и дата конца периода
    """
    start_years_ago = (datetime.today() - timedelta(days=year_ago * 365)).strftime("%Y-%m-%d")
    end_years_ago = (datetime.today() - timedelta(days=(year_ago-1) * 365 + 1)).strftime("%Y-%m-%d")
    return start_years_ago, end_years_ago


def check_and_create_folder(path):
    """
    Проверка на существование папки и создание папки, если не существует
    :param path: путь к папке
    """
    if not os.path.exists(path):
        os.mkdir(data_path)


def get_main_data(ticker_list):
    # из-за ограничений в API МосБиржи отправляю несколько запросов
    # расчетный период - сегодняшняя дата минус 10 лет
    # 1 котировка за месяц
    print(ticker_list)
    rows = list()

    for ticker in ticker_list:
        frames = list()
        for year in range(10, 0, -1):
            start, end = get_start_and_end_dates(year)
            df = get_data_by_date(start, end, ticker)
            if df is not None:
                frames.append(df)

        if len(frames) == 0:
            print(f'\t\tTicker: {ticker}, rows: {len(frames)} - CONTINUE')
            continue
        else:
            print(f'Ticker: {ticker}, rows: {len(frames)}')

        result = pd.concat(frames).drop_duplicates(subset=['TRADEDATE']).set_index('TRADEDATE')
        new_row = result.transpose()
        new_row['ticker'] = ticker
        new_row.set_index('ticker', inplace=True)

        rows.append(new_row)

        # if ticker == 'SBER':
        #     df_for_reindex = result

    return pd.concat(rows, axis=0)


def save_main_df(df):
    """
    Сохранение полученных данных в файл
    :param df: котировки в формате DataFrame
    """
    df.to_csv(os.path.join(ROOT, data_path, main_data_path))


def download_data():
    check_and_create_folder(data_path)
    tickers = get_tickers(os.path.join(ROOT, data_path, ticker_file_path))
    result_df = get_main_data(tickers)
    save_main_df(result_df)
