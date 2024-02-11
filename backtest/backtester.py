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
