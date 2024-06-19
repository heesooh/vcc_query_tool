import pandas as pd
from data import get_records
from filter import filter_records
from revenue import calculate_card_revenue
from gsheet import gsheet_write

if __name__ == '__main__':
    # records = get_records('2024-05-01', '2024-05-31')
    # filtered_records = filter_records(records)
    # updated_records = calculate_card_revenue(filtered_records)

    # updated_records['apply_records'].to_csv("../data/apply_records.csv", index=False)
    # updated_records['recharge_records'].to_csv("../data/recharge_records.csv", index=False)
    # updated_records['underpaid_records'].to_csv("../data/underpaid_records.csv", index=False)
    # updated_records['error_records'].to_csv("../data/error_records.csv", index=False)
    # updated_records['test_records'].to_csv("../data/test_records.csv", index=False)

    # print(updated_records['apply_records'].to_string())
    # print(updated_records['recharge_records'].to_string())
    # print(updated_records['underpaid_records'].to_string())
    # print(updated_records['error_records'].to_string())
    # print(updated_records['test_records'].to_string())

    # apply_records = pd.read_csv("../data/apply_records.csv")
    # recharge_records = pd.read_csv("../data/recharge_records.csv")
    # underpaid_records = pd.read_csv("../data/underpaid_records.csv")
    # error_records = pd.read_csv("../data/error_records.csv")
    # test_records = pd.read_csv("../data/test_records.csv")

    # print(apply_records.to_string())
    # print(recharge_records.to_string())
    # print(underpaid_records.to_string())
    # print(error_records.to_string())
    # print(test_records.to_string())

    gsheet_write()
