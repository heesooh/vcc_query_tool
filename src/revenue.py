from data import get_pending_records

min_top_up_amount = 20
mw_tx_fee_percent = 0.015
as_tx_fee_percent = 0.015
as_application_amount = 5


def _apply_revenue(records):
    for index, record in records.iterrows():
        records.at[index, 'mw_apply_amount'] = record['base_amount'] - as_application_amount
        records.at[index, 'as_apply_amount'] = as_application_amount

        records.at[index, 'top_up_amount'] = min_top_up_amount
        records.at[index, 'mw_tx_fee'] = min_top_up_amount * mw_tx_fee_percent
        records.at[index, 'as_tx_fee'] = min_top_up_amount * as_tx_fee_percent

        records.at[index, 'overpaid_amount'] = record['paid_amount'] - record['requested_amount']

    return records


def _recharge_revenue(records):
    for index, record in records.iterrows():
        records.at[index, 'recharge_amount'] = record['base_amount']

        records.at[index, 'mw_tx_fee'] = record['base_amount'] * mw_tx_fee_percent
        records.at[index, 'as_tx_fee'] = record['base_amount'] * as_tx_fee_percent

        records.at[index, 'overpaid_amount'] = record['paid_amount'] - record['requested_amount']

    return records


def _update_pending_records(prev, curr):
    prev = prev.sort_values(by=['order_id'])
    curr = curr.sort_values(by=['order_id'])

    common_columns = prev.columns.intersection(curr.columns)

    for column in common_columns:
        prev[column] = curr[column]

    return prev


def _underpaid_revenue(records):
    pending_records = get_pending_records(records['order_id'].astype(str).tolist())
    updated_records = _update_pending_records(records, pending_records)

    for index, record in updated_records.iterrows():
        updated_records.at[index, 'underpaid_amount'] = record['paid_amount']
        updated_records.at[index, 'missing_amount'] = record['requested_amount'] - record['paid_amount']

    return updated_records


def calculate_card_revenue(records):
    apply_records = _apply_revenue(records['apply_records'])
    recharge_records = _recharge_revenue(records['recharge_records'])
    underpaid_records = _underpaid_revenue(records['underpaid_records'])

    return {
        'apply_records': apply_records,
        'recharge_records': recharge_records,
        'underpaid_records': underpaid_records,
        'error_records': records['error_records'],
        'test_records': records['test_records']
    }
