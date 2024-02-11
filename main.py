import pandas as pd
from settings import PATH_TO_TMP
from tabulate import tabulate
import logging
from backtest import backtester
import stock_selector.funcs
from stock_selector.funcs import finviz_get_tickers_as_list, yfinance_get_historic_data
from tabulate import tabulate
from technical_analysis import ta_funcs
from trade_builder.sl_rules import tbs_first_candle_close_hard
from trade_builder.tp_rules import tbs_three_to_one

#filters = ["idx_sp500"]
#sp_500 = finviz_get_tickers_as_list(filters=filters, save_to_tmp=True, order=[])
#ticker_price_data = yfinance_get_historic_data(ticker_list=sp_500,
#                                               interval="1d",
#                                               period="5y", save_to_tmp=True)

# Set logging level:
logging.basicConfig(level=logging.INFO)



price_rawdf = pd.read_csv(f"{PATH_TO_TMP}/yahoo_ticklist_price_data_2024-02-07.csv", header=[0, 1], index_col=0)
ticker_list = list(price_rawdf.columns.get_level_values(1).unique())

# Stores the dataframes that should be passed to the backtester for simulating execution of trades.
ticker_data_w_trades = {}

for ticker in ticker_list:
    logging.info(f"Analysing {ticker}...")
    ticker_data = price_rawdf.xs(ticker, level=1, axis=1).reset_index()
    results = ta_funcs.iterate_three_bar_spring(price_df=ticker_data, drop_percentage=-1)

    # If dataframe contains any valid trades:
    if results["Three_bar_spring"].any():
        logging.info(f"{ticker} has >= 1 valid trade.")

        # Add Stop loss and take profit values for each trade.
        results = tbs_first_candle_close_hard(price_df=results)
        results = tbs_three_to_one(price_df=results)

        # Set SL and TP value.- Can add more into here for dynamic SL etc.
        # Adds a key:value pair to a dict containing the ticker name and the price_df with associated valid trades.
        ticker_data_w_trades[ticker] = results

# Pass to backtester.
backtester = backtester.Backtester(price_df_dict=ticker_data_w_trades,
                                   max_sl=1,
                                   max_tp=3,
                                   init_bankroll=1000,
                                   )
test = backtester.get_results()


#print(tabulate(backtester.sort_trades_by_date(), headers="keys"))


