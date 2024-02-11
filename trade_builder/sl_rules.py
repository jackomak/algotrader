# Functions for setting stop loss levels. All functions take a dataframe as an input

def tbs_first_candle_close_hard(price_df):
    spring_rows = price_df.index[price_df["Three_bar_spring"] == True].tolist()

    for index in spring_rows:
        drop_row = index - 2
        # Don't need an if statement here as Spring wont be marked true if data is missing from
        #  beginning of index.
        price_df.loc[spring_rows, "Stop_loss"] = price_df.loc[drop_row, "Close"]

        return price_df