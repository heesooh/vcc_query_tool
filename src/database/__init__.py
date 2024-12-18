from .query import get_payment_gateway_records, get_card_records
import pandas as pd


def _merge_records(payment_gateway_records, card_records):
    card_records['order_id'] = pd.to_numeric(card_records['order_id'], errors='coerce').astype('int64')
    return pd.merge(payment_gateway_records, card_records, how='left', on='order_id')


def get_records(from_date, to_date):
    payment_gateway_records = get_payment_gateway_records(from_date, to_date)
    card_records = get_card_records(from_date, to_date)

    return _merge_records(payment_gateway_records, card_records)
