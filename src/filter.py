import os
from scraper import *
from dotenv import load_dotenv
from tqdm import tqdm

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


def _remove_prefix(apply_records, recharge_records):
    apply_records.loc[:, 'order_type'] = 'APPLY_CARD'
    recharge_records.loc[:, 'order_type'] = 'RECHARGE_CARD'

    return apply_records, recharge_records


def _reset_index(records):
    for _, record in records.items():
        record.reset_index(drop=True, inplace=True)

    return records


def _filter_client_test_records(records):
    client_records = records[records['is_client']]
    test_records = records[~records['is_client']]

    client_records_success = client_records[client_records['order_status'] == 'SUCCESS']
    client_records_pending = client_records[client_records['order_status'].isnull()]

    card_apply_records = client_records_success[client_records_success['order_type'] == 'BP_APPLY_CARD']
    card_recharge_records = client_records_success[client_records_success['order_type'] == 'BP_RECHARGE_CARD']

    client_underpaid_records = client_records_pending[client_records_pending['pay_status'] == 0]
    client_error_records = client_records_pending[client_records_pending['pay_status'] != 0]

    card_apply_records, card_recharge_records = _remove_prefix(card_apply_records, card_recharge_records)

    filtered_records = {
        'apply_records': card_apply_records,
        'recharge_records': card_recharge_records,
        'underpaid_records': client_underpaid_records,
        'error_records': client_error_records,
        'test_records': test_records
    }

    return _reset_index(filtered_records)


def filter_records(records):
    progress = tqdm(total=records.shape[0])
    records['is_client'] = None

    for index, record in records.iterrows():
        sender_address = _get_sender_address(record['transaction_hash'])
        progress.update()
        records.at[index, 'sender_address'] = sender_address

        if _is_test_address(sender_address):
            records.at[index, 'is_client'] = False
        else:
            records.at[index, 'is_client'] = True

    progress.close()
    records['is_client'] = records['is_client'].astype(bool)

    return _filter_client_test_records(records)
