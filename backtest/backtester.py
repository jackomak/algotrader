import logging
from tabulate import tabulate

import pandas as pd

res_headers = ["trade_no", "ticker", "day_of_week", "date_exe", "date_stopped", "start_br", "end_br", "percent_gl",
               "cum_gl", "trade_outcome"]


class Backtester:
    """
    Takes a dictionary, with key:values in the following order: ticker: price_df. Where price_df has the following columns:
    [['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume', 'Three_bar_spring']]
    """

    def __init__(self, price_df_dict, max_sl, max_tp, init_bankroll):
        self.max_sl = max_sl
        self.max_tp = max_tp
        self.init_bankroll = init_bankroll
        self.price_df_dict = price_df_dict
        self.tickers = price_df_dict.keys()
        self.result_df = pd.DataFrame(columns=res_headers)
        self.date_sorted_trades = self.sort_trades_by_date()

    def sort_trades_by_date(self):
        valid_trades = pd.DataFrame()

        for key, df in self.price_df_dict.items():
            df["Source"] = key

            # Find trade rows.
            valid_trade_rows = df[df["Three_bar_spring"] == True]
            valid_trades = pd.concat([valid_trades, valid_trade_rows], ignore_index=True)

            # Sort by date.
            valid_trades['Date'] = pd.to_datetime(valid_trades['Date'])
            date_sorted_trades = valid_trades.sort_values(by="Date")

        return date_sorted_trades

    def analyse_trade(self, row):
        ticker = row["Source"]
        date = pd.to_datetime(row["Date"])

        # Get the relevant dataframe and splice it to only include relevant rows.
        price_df = self.price_df_dict[ticker]
        df_from_trade_start = price_df[pd.to_datetime(price_df["Date"]) >= date].copy().reset_index()

        # Set end params.
        stop_loss = round(df_from_trade_start["Stop_loss"].iloc[0], 2)
        take_profit = round(df_from_trade_start["Take_profit"].iloc[0], 2)

        # Check each row in turn for a trade outcome.
        logging.info(
            f"[Analysing trade for TICKER: {ticker}, DATE: {date}, STOPLOSS: {stop_loss}, TAKEP:{take_profit}.]")

        for index, row in df_from_trade_start.iterrows():
            outcome = "none"

            # If buying on close of day.
            if index == 0:
                continue

            if row["Low"] <= stop_loss:
                logging.info(f"[Day {index}]. Stop loss hit for trade {date} TICKER: {ticker}.")
                outcome = "lose"
                break

            if row["High"] >= take_profit:
                logging.info(f"[Day {index}]. Take profit hit for trade {date} TICKER: {ticker}.")
                outcome = "win"
                break

            else:
                logging.info(f"[Day {index}]. Trade in progress.")
                outcome = "ongoing"

        return outcome

    def get_results(self):
        bankroll_vals = []
        for index, row in self.date_sorted_trades.iterrows():
            outcome = self.analyse_trade(row)

            # Update the bankroll with respect to the trade outcomes.
            if outcome == "lose":
                self.init_bankroll = self.init_bankroll * 0.99

            if outcome == "win":
                self.init_bankroll = self.init_bankroll * 1.03

            logging.info(f"BANKROLL: {self.init_bankroll}")
            bankroll_vals.append(self.init_bankroll)

        print(bankroll_vals)
