def tbs_three_to_one(price_df):
    price_df.loc[price_df["Three_bar_spring"] == True, "Take_profit"] =\
        round(price_df["Close"] + ((price_df["Close"] - price_df["Stop_loss"]) * 3), 2)
    return price_df