import pandas as pd
from settings import PATH_TO_TMP
from tabulate import tabulate
import logging

import stock_selector.funcs
from stock_selector.funcs import finviz_get_tickers_as_list, yfinance_get_historic_data
from tabulate import tabulate
from technical_analysis import ta_funcs

filters = ["idx_sp500"]
# sp_500 = finviz_get_tickers_as_list(filters=filters, save_to_tmp=True, order=[])
# ticker_price_data = yfinance_get_historic_data(ticker_list=sp_500,
#                                               interval="1d",
#                                               period="1mo", save_to_tmp=True)


price_rawdf = pd.read_csv(f"{PATH_TO_TMP}/yahoo_ticklist_price_data_2024-02-07.csv", header=[0, 1], index_col=0)
ticker_list = list(price_rawdf.columns.get_level_values(1).unique())

# Stores the dataframes that should be passed to the backtester for simulating execution of trades.
tickers_with_trades = []

for ticker in ticker_list:
    logging.info(f"Analysing {ticker}...")
    ticker_data = price_rawdf.xs(ticker, level=1, axis=1).reset_index()
    results = ta_funcs.iterate_three_bar_spring(price_df=ticker_data, drop_percentage=-1)

    if results is not None:
        print(f"==={ticker}===")
        print(tabulate(results, headers="keys"))