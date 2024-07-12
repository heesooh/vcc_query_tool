import os
from dotenv import load_dotenv
from query import get_pending_records

load_dotenv()

min_top_up_amount = float(os.getenv('MIN_TOP_UP_AMOUNT'))
as_card_apply_amount = float(os.getenv('AS_CARD_APPLY_FEE'))
recharge_fee_percent = float(os.getenv('RECHARGE_FEE_RATE'))
as_recharge_fee_percent = float(os.getenv('AS_RECHARGE_FEE_RATE'))


def _get_recharge_fee(top_up_amount):
    as_recharge_fee = top_up_amount * as_recharge_fee_percent
    mw_recharge_fee = top_up_amount * recharge_fee_percent - as_recharge_fee

    return as_recharge_fee, mw_recharge_fee


def _apply_revenue(records):
    for index, record in records.iterrows():
        records.at[index, 'mw_apply_amount'] = record['base_amount'] - as_card_apply_amount
        records.at[index, 'as_apply_amount'] = as_card_apply_amount

        records.at[index, 'top_up_amount'] = min_top_up_amount

        as_tx_fee, mw_tx_fee = _get_recharge_fee(min_top_up_amount)

        records.at[index, 'as_tx_fee'] = as_tx_fee
        records.at[index, 'mw_tx_fee'] = mw_tx_fee

        records.at[index, 'overpaid_amount'] = record['paid_amount'] - record['order_amount']

    return records


def _recharge_revenue(records):
    for index, record in records.iterrows():
        records.at[index, 'recharge_amount'] = record['base_amount']

        as_tx_fee, mw_tx_fee = _get_recharge_fee(float(record['base_amount']))

        records.at[index, 'as_tx_fee'] = as_tx_fee
        records.at[index, 'mw_tx_fee'] = mw_tx_fee

        records.at[index, 'overpaid_amount'] = record['paid_amount'] - record['order_amount']

    return records


def _update_pending_records(prev, curr):
    prev = prev.sort_values(by=['order_id'])
    curr = curr.sort_values(by=['order_id'])

    common_columns = prev.columns.intersection(curr.columns)

    for column in common_columns:
        prev[column] = curr[column]

    return prev


def _underpaid_revenue(records):
    records['underpaid_amount'] = None
    records['missing_amount'] = None

    if not records.empty:
        pending_records = get_pending_records(records['order_id'].astype(str).tolist())
        updated_records = _update_pending_records(records, pending_records)

        for index, record in updated_records.iterrows():
            updated_records.at[index, 'underpaid_amount'] = record['paid_amount']
            updated_records.at[index, 'missing_amount'] = record['order_amount'] - record['paid_amount']

        return updated_records

    return records


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
