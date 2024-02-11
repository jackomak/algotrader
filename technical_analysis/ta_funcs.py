import pandas as pd
import logging


def calculate_percent_change(open_value, close_value):
    """
    calculates the % change between two values, typically for calculating the difference between the open and close
    of a candle in percentage.

    :param open_value:
    :param close_value:
    :return: float
    """
    percent_change = ((close_value - open_value) / open_value) * 100
    logging.info(f"Percentage change of {open_value} To {close_value} : {percent_change} %")
    return percent_change


def slice_price_matrix(price_df, index, number_of_rows: int):
    """
    Slices a dataframe to get the number of subsequent requested rows (number_of_rows) from the index supplied as
    an argument. First row in pandas dataframe has a matrix of zero. e.g. slice_price_matrix(price_df, 0, 3) will return
    the first three rows of the dataframe.

    :param price_df:
    :param index:
    :param number_of_rows:
    :return:
    """
    sliced_price_df = price_df.iloc[index:index + number_of_rows]

    try:
        assert len(sliced_price_df) == number_of_rows
        return sliced_price_df

    except AssertionError as e:
        if index > len(sliced_price_df - 1):
            logging.info("Index supplied is larger than number of rows in dataframe (-1).")
        else:
            # Dataframe will return empty if index supplied is larger than the number of rows in the dataframe (-1) as
            # it is zero based.
            logging.info("Sliced dataframe != number of rows. Input dataframe too small?")


def identify_three_bar_spring(three_row_df, drop_value_percentage: float):
    """
    Analyses a price info dataframe for the appearance of a three-bar wykoff spring pattern. The drop_value of the
    spring is the difference between the 1st candle open and the 1st candle close. This function assesses the price
    information of the df["index"] as the 1st "drop" candle and the next two rows as the "spring" and "thrust" candle.
    using the following rules:

    1. Distance between "drop" candle open and close must be > the specified drop_value.
    2. Spring candle close must be < drop candle close.
    3. Thrust candle close must be > drop candle open.

    Headers of dataframe must include: headers labeled "Close" and "Open".
    :param index: Int
    :param drop_value_percentage: float eg 1.2 for 1.2%, -0.5 for -0.5%.
    :return: Boolean
    """

    # Rule 1.
    drop_candle = three_row_df.iloc[0]
    drop_candle_distance = calculate_percent_change(drop_candle["Open"], drop_candle["Close"])
    if drop_candle_distance > drop_value_percentage:
        logging.info(f"{drop_candle_distance} Drop distance not long enough.")
        return False

    # Rule 2.
    spring_candle = three_row_df.iloc[1]
    if spring_candle["Close"] > drop_candle["Close"]:
        logging.info("Spring candle is Green.")
        return False

    # Rule 3.
    thrust_candle = three_row_df.iloc[2]
    if thrust_candle["Close"] < drop_candle["Open"]:
        logging.info(f"Thrust candle close is less than drop candle open.")
        return False

    # If all three rules pass.
    logging.info("Found valid pattern.")
    return True


def iterate_three_bar_spring(price_df, drop_percentage):
    """
    Iterates through each index of a price_df. Analyses in a sliding window for Three bar spring pattern. Final two
    rows of the dataframe are removed as this will result in incomplete patterns. Headers of dataframe must include:
    headers labeled "Close" and "Open". Returns the dataframe with a new column "Three_bar_spring" that will be set to
    True if the candle is the opening bar of the three bar spring... This dataframe can then be passed to a backtester.
    :param price_df.
    :param drop_percentage.
    :return: pandas dataframe.
    """
    # Get length of dataframe and build list of iloc numbers up to the length from 0 to n-2. F
    # Final two rows as these will have incomplete patterns.
    selected_rows = []

    price_df["Three_bar_spring"] = False

    for index, row in price_df[:-2].iterrows():
        sliced_rows = slice_price_matrix(price_df, index, number_of_rows=3)
        is_valid_pattern = identify_three_bar_spring(sliced_rows, drop_percentage)

        if is_valid_pattern:
            price_df.at[index, "Three_bar_spring"] = True

    try:

        return price_df

    except ValueError as e:
        logging.info("Found 0 Three bar springs in dataframe.")
        return None
# Session.
# ig_service = igpi.login_to_ig()

# igpi.get_historical_data(ig_service, epic="CS.D.EURUSD.MINI.IP", resolution='H', num_points=100, save_as_tmp=True)
# msft_df = pd.read_csv("../tmp/MSFT_D_126_rows.csv", header=[0, 1], index_col=0)
# valid_rows = iterate_three_bar_spring(msft_df, drop_percentage=-0.5)
# print(tabulate(valid_rows, headers="keys"))
