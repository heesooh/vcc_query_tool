import os
from scraper import *
from mysql_data import *
from dotenv import load_dotenv

load_dotenv()
test_account_1 = os.getenv('INTERNAL_ADDRESS_1')
test_account_2 = os.getenv('INTERNAL_ADDRESS_2')
test_account_3 = os.getenv('INTERNAL_ADDRESS_3')
test_account_4 = os.getenv('INTERNAL_ADDRESS_4')
test_account_5 = os.getenv('INTERNAL_ADDRESS_5')


def is_erc_address(address):
    return address.startswith('0x')


def is_test_address(address):
    test_addresses = [
        test_account_1,
        test_account_2,
        test_account_3,
        test_account_4,
        test_account_5
    ]

    return address in test_addresses

df1 = payment_records('2024-05-01', '2025-05-31')
df2 = card_records()
records = merge_records(df1, df2)

# TODO: FIX THIS
def order_filter(records):
    for index, record in records.iterrows():
        curr_hash = record['tx_id']
        if (is_erc_address(curr_hash)):
            sender_address = get_erc_sender_address(curr_hash)
        else:
            sender_address = get_trc_sender_address(curr_hash)

        print(sender_address)


order_filter(records)

