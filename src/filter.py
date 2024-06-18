import os
from scraper import *
from dotenv import load_dotenv

load_dotenv()

test_account_1 = os.getenv('INTERNAL_ADDRESS_1')
test_account_2 = os.getenv('INTERNAL_ADDRESS_2')
test_account_3 = os.getenv('INTERNAL_ADDRESS_3')
test_account_4 = os.getenv('INTERNAL_ADDRESS_4')
test_account_5 = os.getenv('INTERNAL_ADDRESS_5')


def _get_sender_address(hash_id):
    if hash_id.startswith('0x'):
        sender_address = get_erc_sender_address(hash_id)
    else:
        sender_address = get_trc_sender_address(hash_id)

    return sender_address


def _is_test_address(address):
    test_addresses = [
        test_account_1,
        test_account_2,
        test_account_3,
        test_account_4,
        test_account_5
    ]

    return address in test_addresses


def _estimate_filter_time(records):
    total_num = records.shape[0]
    estimated_time = (total_num / 10) * 4.77
    print(f"Filtering a total of {total_num} records...")
    print(f"Estimated filtering time: {estimated_time} seconds")


def _filter_client_test_records(records):
    client_records = records[records['is_client']]
    test_records = records[~records['is_client']]

    client_records_success = client_records[client_records['order_status'] == 'SUCCESS']
    client_records_pending = client_records[client_records['order_status'].isnull()]

    card_apply_records = client_records_success[client_records_success['order_type'] == 'BP_APPLY_CARD']
    card_recharge_records = client_records_success[client_records_success['order_type'] == 'BP_RECHARGE_CARD']

    return card_apply_records, card_recharge_records, client_records_pending, test_records


def filter_records(records):
    _estimate_filter_time(records)

    for index, record in records.iterrows():
        sender_address = _get_sender_address(record['tx_id'])
        records.at[index, 'sender_address'] = sender_address

        if _is_test_address(sender_address):
            records.at[index, 'is_client'] = False
        else:
            records.at[index, 'is_client'] = True

    records['is_client'] = records['is_client'].astype(bool)

    return _filter_client_test_records(records)
