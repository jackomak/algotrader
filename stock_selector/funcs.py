import logging
import sys
from settings import PATH_TO_TMP
from finviz.screener import Screener
from datetime import date
import os
import yfinance as yf


# Instantiate screener with the relevent filters.
filters = ["cap_midover", "exch_nasd", "ta_sma200_pa"]
order = "perf1w"


def finviz_get_tickers_as_list(filters: list, order: str, save_to_tmp=False):
    """
    Returns a list of stock tickers from FinViz filtered by values supplied as arguments. The order of the stocks
    can be specified by the order argument.
    :param filters:
    :param order:
    :param save_to_tmp:
    :return:
    """
    timestamp = date.today()
    logging.info("Parsing Finviz and downloading data:")
    stock_list = Screener(filters=filters, order=order, table="Overview")
    if save_to_tmp:
        stock_list.to_csv(f"{PATH_TO_TMP}/finviz_stock_list_{timestamp}.csv")

    ticker_list = []
    for stock in stock_list:
        ticker_list.append(stock["Ticker"])

    return ticker_list


def yfinance_get_historic_data(ticker_list: list, interval: str, period: str, save_to_tmp=False):
    """
    Returns price information for a list of specified tickers. Interval and period can be set. Returns a multi-level
    pandas dataframe that must undergo further formatting to pull all information for a single ticker.
    :param ticker_list: list
    :param interval: str eg "1d"
    :param period: str
    :param save_to_tmp: bool
    :return: pandas.dataframe
    """
    logging.info("Downloading data from Yahoo Finance:")
    ticker_price_data = yf.download(ticker_list, period=period, interval=interval, rounding=True, progress=True)

    if save_to_tmp:
        cwd = os.getcwd()
        ticker_price_data.to_csv(f"{PATH_TO_TMP}/yahoo_ticklist_price_data_{date.today()}.csv")

    return ticker_price_data
