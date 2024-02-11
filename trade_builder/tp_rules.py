def tbs_multiple_of_dcc(price_df, profit_factor: int):
    price_df.loc[price_df["Three_bar_spring"] == True, "Take_profit"] =\
        price_df["Close"] + ((price_df["Close"] - price_df["Stop_loss"]) * profit_factor)
    return price_df