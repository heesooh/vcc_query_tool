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
test_account_6 = os.getenv('INTERNAL_ADDRESS_6')


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
        test_account_5,
        test_account_6
    ]

    return address in test_addresses


def _update_record_column(records, column_name, value):
    records.loc[:, column_name] = value
    return records


def _reset_index(records):
    for _, record in records.items():
        record.reset_index(drop=True, inplace=True)

    return records


def _filter_client_test_records(records):
    client_records = records[~records['test_account']]
    test_records = records[records['test_account']]

    pending_records = client_records[client_records['order_status'] == 0]
    _update_record_column(pending_records, 'order_status', "PENDING")

    success_records = client_records[client_records['order_status'] == 1]
    _update_record_column(success_records, 'order_status', "SUCCESS")

    timeout_records = client_records[client_records['order_status'] == 2]
    _update_record_column(timeout_records, 'order_status', "TIMEOUT")

    cancelled_records = client_records[client_records['order_status'] == 3]
    _update_record_column(cancelled_records, 'order_status', "CANCELLED")

    refund_records = client_records[client_records['order_status'] == 4]
    _update_record_column(refund_records, 'order_status', "REFUND")

    apply_records = success_records[success_records['order_type'].str.contains('APPLY', na=False)]
    _update_record_column(apply_records, 'order_type', "APPLY")
    recharge_records = success_records[success_records['order_type'].str.contains('RECHARGE', na=False)]
    _update_record_column(recharge_records, 'order_type', "RECHARGE")

    filtered_records = {
        'pending': pending_records,
        'apply': apply_records,
        'recharge': recharge_records,
        'cancelled': cancelled_records,
        'timeout': timeout_records,
        'refund': refund_records,
        'test': test_records
    }

    return _reset_index(filtered_records)


def filter_records(records):
    records = records[~records['notify_url'].str.contains('polyflow', na=False)]

    progress = tqdm(total=records.shape[0])
    records['test_account'] = None

    for index, record in records.iterrows():
        sender_address = _get_sender_address(record['tx_id'])
        progress.update()
        records.at[index, 'sender_address'] = sender_address

        if _is_test_address(sender_address):
            records.at[index, 'test_account'] = True
        else:
            records.at[index, 'test_account'] = False

        if record['card_issuer'] is None:
            if 'BP' in record['order_type']:
                records.at[index, 'card_issuer'] = 'BP'
            elif 'EE' in record['order_type']:
                records.at[index, 'card_issuer'] = 'EE'
            elif 'FO' in record['order_type']:
                records.at[index, 'card_issuer'] = 'FO'

        if record['pay_status'] == 0:
            records.at[index, 'pay_status'] = 'Insufficient Payment'
        elif record['pay_status'] == 1:
            records.at[index, 'pay_status'] = 'Full Payment'
        elif record['pay_status'] == 2:
            records.at[index, 'pay_status'] = 'Over Payment'

    progress.close()
    records['test_account'] = records['test_account'].astype(bool)

    return _filter_client_test_records(records)
