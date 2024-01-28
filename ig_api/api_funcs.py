from trading_ig import IGService
import pandas as pd
from tabulate import tabulate

# globals.
USERNAME = "jackomak"
PASSWORD = "StPeters0328!"
ACCOUNT_TYPE = "demo"
API_KEY = "c710ae469e26ac3513ea08bd131777aaf8c4f39b"
TEMP_DIRECTORY = "../tmp"


def login_to_ig(username=USERNAME, password=PASSWORD, api_key=API_KEY, acc_type=ACCOUNT_TYPE):
    ig_service = IGService(username, password, api_key, acc_type)
    try:
        ig_service.create_session()
        print("Login successful.")
        return ig_service

    except Exception as e:
        print("An error occurred during login:", e)
        return None


def get_historical_data(session, epic, resolution, num_points, save_as_tmp=False):
    try:
        response = session.fetch_historical_prices_by_epic_and_num_points(epic, resolution, num_points)
        historical_data = response['prices']

        if save_as_tmp:
            historical_data.to_csv(f"{TEMP_DIRECTORY}/{epic}_{response}_{num_points}_rows.csv")

        return historical_data
    except Exception as e:
        print("An error occurred while fetching historical data:", e)
        return None
