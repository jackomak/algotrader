import pandas as pd
from tabulate import tabulate
from technical_analysis import ta_funcs

test_data = pd.read_csv("./tmp/MSFT_D_126_rows.csv", header=[0, 1], index_col=0)
print(test_data)
test_data.columns = ["Date", "Open", "High", "Low", "Close", "Aopen", "Volume"]

test = ta_funcs.iterate_three_bar_spring(test_data, -1)
print(test)
