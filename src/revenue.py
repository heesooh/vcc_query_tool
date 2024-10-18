import os
from dotenv import load_dotenv

load_dotenv()

min_top_up_amount = float(os.getenv('MIN_TOP_UP_AMOUNT'))
as_card_apply_amount = float(os.getenv('AS_CARD_APPLY_FEE'))
recharge_fee_percent = float(os.getenv('RECHARGE_FEE_RATE'))
as_recharge_fee_percent = float(os.getenv('AS_RECHARGE_FEE_RATE'))

mw_card = {
    'BP_APPLY_FEE': 19,
    'EE_APPLY_FEE': 99,
    'FO_APPLY_FEE': 9,
    'RECHARGE_FEE': 0.03,
    'MIN_TOP_UP': 20,
    # 'AS_APPLY_FEE': 5,
    # 'AS_RECHARGE_FEE': 0.017
}
u_card = {
    'BP_APPLY_FEE': 120,
    'EE_APPLY_FEE': 99,
    'FO_APPLY_FEE': 12,
    'RECHARGE_FEE': 0.03,
    'MIN_TOP_UP': 20,
    # 'AS_APPLY_FEE': 5,
    # 'AS_RECHARGE_FEE': 0.017
}
kim_card = {
    'BP_APPLY_FEE': 0,  # Kim Card Does Not Support BlockPurse
    'EE_APPLY_FEE': 99,
    'FO_APPLY_FEE': 9,
    'RECHARGE_FEE': 0.04,
    'MIN_TOP_UP': 20,
    # 'AS_APPLY_FEE': 5,
    # 'AS_RECHARGE_FEE': 0.017
}
ton_card = {
    'BP_APPLY_FEE': 25,
    'EE_APPLY_FEE': 0,  # Ton Card Does Not Support EasyEuro
    'FO_APPLY_FEE': 0,  # Ton Card Does Not Support FinancialOne
    'RECHARGE_FEE': 0.03,
    'MIN_TOP_UP': 20,
    # 'AS_APPLY_FEE': 5,
    # 'AS_RECHARGE_FEE': 0.017
}

def _get_recharge_fee(top_up_amount):
    as_recharge_fee = top_up_amount * as_recharge_fee_percent
    mw_recharge_fee = top_up_amount * recharge_fee_percent - as_recharge_fee

    return as_recharge_fee, mw_recharge_fee


def _calculate_revenue_helper(record, card, is_apply):
    if is_apply:
        if 'BP' in record['service']:
            # TODO: Calculate AS and MW apply commissions
            record['apply_commission'] = card['BP_APPLY_FEE']
        elif 'EE' in record['service']:
            # TODO: Calculate AS and MW apply commissions
            record['apply_commission'] = card['EE_APPLY_FEE']
        elif 'FO' in record['service']:
            # TODO: Calculate AS and MW apply commissions
            record['apply_commission'] = card['FO_APPLY_FEE']

    record['top_up_amount'] = record['order_amount_before_fee']
    # TODO: Calculate AS and MW top up commissions
    record['top_up_commission'] = record['order_amount_before_fee'] * card['RECHARGE_FEE']
    record['overpaid_payment_amount'] = record['paid_amount'] - record['order_amount_after_fee']

    return record


def _calculate_revenue(records, is_apply):
    if is_apply: records['apply_commission'] = None
    records['top_up_amount'] = None
    records['top_up_commission'] = None
    records['overpaid_payment_amount'] = None

    for index, record in records.iterrows():
        new_record = None
        if 'MW CARD' in record['card_project']:
            new_record = _calculate_revenue_helper(record, mw_card, is_apply)
        elif 'U CARD' in record['card_project']:
            new_record = _calculate_revenue_helper(record, u_card, is_apply)
        elif 'FO CARD' in record['card_project']:
            new_record = _calculate_revenue_helper(record, u_card, is_apply)
        elif 'TON CARD' in record['card_project']:
            new_record = _calculate_revenue_helper(record, ton_card, is_apply)

        records.loc[index] = new_record

    return records


def _update_pending_records(prev, curr):
    prev = prev.sort_values(by=['order_id'])
    curr = curr.sort_values(by=['order_id'])

    common_columns = prev.columns.intersection(curr.columns)

    for column in common_columns:
        prev[column] = curr[column]

    return prev


def calculate_card_revenue(records):
    records['apply'] = _calculate_revenue(records['apply'], True)
    records['recharge'] = _calculate_revenue(records['recharge'], False)

    return records
