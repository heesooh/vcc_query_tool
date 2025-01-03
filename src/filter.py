from scraper import get_sender_address
from tqdm import tqdm
from config import get_internal_address


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


def _is_internal_address(address):
    internal_address = get_internal_address()
    return address in internal_address


def _is_polyflow_record(record):
    return 'polyflow' in record['notify_url']


def _is_valid_issuer(record):
    return 'FO' in record['order_type']


def _pay_status_string_convert(record):
    if record['pay_status'] == 0:
        return 'Insufficient Payment'
    elif record['pay_status'] == 1:
        return 'Full Payment'
    elif record['pay_status'] == 2:
        return 'Over Payment'


def _order_status_string_convert(record):
    if record['order_status'] == 0:
        return 'Pending'
    elif record['order_status'] == 1:
        return 'Success'
    elif record['order_status'] == 2:
        return 'Timeout'
    elif record['order_status'] == 3:
        return 'Cancelled'
    elif record['order_status'] == 4:
        return 'Refund'


def filter_records(records):

    # progress = tqdm(total=records.shape[0])
    # records['test_account'] = None

    # print('Hello')
    # print('Result: ', records)

    for index, record in records.iterrows():
        address = get_sender_address(record['tx_id'])
        if _is_internal_address(address) or _is_polyflow_record(record) or not _is_valid_issuer(record):
            continue
        else:
            record['sender_address'] = address
            record['pay_status'] = _pay_status_string_convert(record)
            record['order_status'] = _order_status_string_convert(record)

            yield record

    return records

    # print(records.to_string())

    # progress.update()

    # records.at[index, 'sender_address'] = address
    #
    # if record['pay_status'] == 0:
    #     records.at[index, 'pay_status'] = 'Insufficient Payment'
    # elif record['pay_status'] == 1:
    #     records.at[index, 'pay_status'] = 'Full Payment'
    # elif record['pay_status'] == 2:
    #     records.at[index, 'pay_status'] = 'Over Payment'

    # progress.close()
    # records['test_account'] = records['test_account'].astype(bool)

    # return _filter_client_test_records(records)
