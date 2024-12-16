import os
from dotenv import load_dotenv

mw_card = {
    'BP_APPLY_FEE': 19,
    'BP_CHANNEL_APPLY_FEE': 1,
    'BP_AS_APPLY_FEE': 0,
    'BP_MW_APPLY_FEE': 0,
    'BP_RECHARGE_RATE': 0.03,
    'BP_CHANNEL_RECHARGE_RATE': 0,
    'BP_AS_RECHARGE_RATE': 0.017,
    'BP_MW_RECHARGE_RATE': 0.013,  # On the account sheet 0.012 but calculated as 0.013 so far
    'BP_MONTHLY_FEE': 3,
    'BP_MIN_TOP_UP': 20,
    
    'EE_APPLY_FEE': 99,
    'EE_CHANNEL_APPLY_FEE': 0,
    'EE_AS_APPLY_FEE': 0,
    'EE_MW_APPLY_FEE': 99,
    'EE_RECHARGE_RATE': 0.03,
    'EE_CHANNEL_RECHARGE_RATE': 0,
    'EE_AS_RECHARGE_RATE': 0.018,
    'EE_MW_RECHARGE_RATE': 0.012,
    'EE_MONTHLY_FEE': 9,
    'EE_MIN_TX_FEE': 0.5,  # Minimum Transaction Fee of 0.5 USD (If 0.5% of the TX amount is less than 0.5 USDT)
    'EE_TX_RATE': 0.5,
    'EE_MIN_TOP_UP': 20,

    'FO_APPLY_FEE': 9,
    'FO_CHANNEL_APPLY_FEE': 4,
    'FO_AS_APPLY_FEE': 0,
    'FO_MW_APPLY_FEE': 5,
    'FO_RECHARGE_RATE': 0.03,
    'FO_CHANNEL_RECHARGE_RATE': 0,
    'FO_AS_RECHARGE_RATE': 0.018,
    'FO_MW_RECHARGE_RATE': 0.012,
    'FO_MONTHLY_FEE': 5,
    'FO_MIN_TOP_UP': 20
}
u_card = {
    'BP_APPLY_FEE': 120,
    'BP_CHANNEL_APPLY_FEE': 0,
    'BP_AS_APPLY_FEE': 5,
    'BP_MW_APPLY_FEE': 115,
    'BP_RECHARGE_RATE': 0.03,
    'BP_CHANNEL_RECHARGE_RATE': 0,
    'BP_AS_RECHARGE_RATE': 0.017,
    'BP_MW_RECHARGE_RATE': 0.013,  # On the account sheet 0.012 but calculated as 0.013 so far
    'BP_MONTHLY_FEE': 3,
    'BP_MIN_TOP_UP': 20,

    'EE_APPLY_FEE': 99,
    'EE_CHANNEL_APPLY_FEE': 0,
    'EE_AS_APPLY_FEE': 0,  # Mountain Wolf already paid 22 USD per card
    'EE_MW_APPLY_FEE': 99,
    'EE_RECHARGE_RATE': 0.03,
    'EE_CHANNEL_RECHARGE_RATE': 0,
    'EE_AS_RECHARGE_RATE': 0.018,
    'EE_MW_RECHARGE_RATE': 0.012,
    'EE_MONTHLY_FEE': 9,
    'EE_MIN_TX_FEE': 0.5,  # Minimum Transaction Fee of 0.5 USD (If 0.5% of the TX amount is less than 0.5 USDT)
    'EE_TX_RATE': 0.5,
    'EE_MIN_TOP_UP': 20,

    'FO_APPLY_FEE': 12,
    'FO_CHANNEL_APPLY_FEE': 4,
    'FO_AS_APPLY_FEE': 3,
    'FO_MW_APPLY_FEE': 5,
    'FO_RECHARGE_RATE': 0.03,
    'FO_CHANNEL_RECHARGE_RATE': 0,
    'FO_AS_RECHARGE_RATE': 0.018,
    'FO_MW_RECHARGE_RATE': 0.012,
    'FO_MONTHLY_FEE': 5,
    'FO_MIN_TOP_UP': 20
}
kim_card = {
    'BP_APPLY_FEE': 0,  # Kim Card Does Not Support BlockPurse
    'BP_CHANNEL_APPLY_FEE': 0,
    'BP_AS_APPLY_FEE': 0,
    'BP_MW_APPLY_FEE': 0,
    'BP_RECHARGE_RATE': 0,
    'BP_CHANNEL_RECHARGE_RATE': 0,
    'BP_AS_RECHARGE_RATE': 0,
    'BP_MW_RECHARGE_RATE': 0,
    'BP_MONTHLY_FEE': 0,
    'BP_MIN_TOP_UP': 20,

    'EE_APPLY_FEE': 99,
    'EE_CHANNEL_APPLY_FEE': 0,
    'EE_AS_APPLY_FEE': 0,  # Mountain Wolf already paid 22 USD per card
    'EE_MW_APPLY_FEE': 99,
    'EE_RECHARGE_RATE': 0.03,
    'EE_CHANNEL_RECHARGE_RATE': 0,
    'EE_AS_RECHARGE_RATE': 0.018,
    'EE_MW_RECHARGE_RATE': 0.012,
    'EE_MONTHLY_FEE': 9,
    'EE_MIN_TX_FEE': 0.5,  # Minimum Transaction Fee of 0.5 USD (If 0.5% of the TX amount is less than 0.5 USDT)
    'EE_TX_RATE': 0.5,
    'EE_MIN_TOP_UP': 20,

    'FO_APPLY_FEE': 12,
    'FO_CHANNEL_APPLY_FEE': 4,
    'FO_AS_APPLY_FEE': 3,
    'FO_MW_APPLY_FEE': 5,
    'FO_RECHARGE_RATE': 0.03,
    'FO_CHANNEL_RECHARGE_RATE': 0,
    'FO_AS_RECHARGE_RATE': 0.018,
    'FO_MW_RECHARGE_RATE': 0.012,
    'FO_MONTHLY_FEE': 5,
    'FO_MIN_TOP_UP': 20
}
ton_card = {
    'BP_APPLY_FEE': 25,
    'BP_CHANNEL_APPLY_FEE': 0,
    'BP_AS_APPLY_FEE': 5,
    'BP_MW_APPLY_FEE': 20,
    'BP_RECHARGE_RATE': 0.03,
    'BP_CHANNEL_RECHARGE_RATE': 0,
    'BP_AS_RECHARGE_RATE': 0.017,
    'BP_MW_RECHARGE_RATE': 0.013,  # On the account sheet 0.012 but calculated as 0.013 so far
    'BP_MONTHLY_FEE': 3,
    'BP_MIN_TOP_UP': 20,

    'EE_APPLY_FEE': 0,  # Ton Card Does Not Support EasyEuro
    'EE_CHANNEL_APPLY_FEE': 0,
    'EE_AS_APPLY_FEE': 0,
    'EE_MW_APPLY_FEE': 0,
    'EE_RECHARGE_RATE': 0,
    'EE_CHANNEL_RECHARGE_RATE': 0,
    'EE_AS_RECHARGE_RATE': 0,
    'EE_MW_RECHARGE_RATE': 0,
    'EE_MONTHLY_FEE': 0,
    'EE_MIN_TX_FEE': 0,
    'EE_TX_RATE': 0,
    'EE_MIN_TOP_UP': 20,

    'FO_APPLY_FEE': 0,  # Ton Card Does Not Support FinancialOne
    'FO_CHANNEL_APPLY_FEE': 0,
    'FO_AS_APPLY_FEE': 0,
    'FO_MW_APPLY_FEE': 0,
    'FO_RECHARGE_RATE': 0,
    'FO_CHANNEL_RECHARGE_RATE': 0,
    'FO_AS_RECHARGE_RATE': 0,
    'FO_MW_RECHARGE_RATE': 0,
    'FO_MONTHLY_FEE': 0,
    'FO_MIN_TOP_UP': 20
}


def _calculate_revenue_helper(record, card, is_apply):
    if is_apply:
        if 'BP' in record['card_issuer']:
            if is_apply:
                record['apply_amount'] = card['BP_APPLY_FEE']
                # record['apply_channel_fee'] = card['BP_CHANNEL_APPLY_FEE']
                # record['apply_as_commission'] = card['BP_AS_APPLY_FEE']
                # record['apply_mw_commission'] = card['BP_MW_APPLY_FEE']
                record['top_up_amount'] = card['BP_MIN_TOP_UP']
                record['top_up_commission'] = card['BP_MIN_TOP_UP'] * card['BP_RECHARGE_RATE']
                # record['top_up_channel_fee'] = card['BP_MIN_TOP_UP'] * card['BP_CHANNEL_RECHARGE_RATE']
                # record['top_up_as_commission'] = card['BP_MIN_TOP_UP'] * card['BP_AS_RECHARGE_RATE']
                # record['top_up_mw_commission'] = card['BP_MIN_TOP_UP'] * card['BP_MW_RECHARGE_RATE']
            else:
                record['top_up_amount'] = record['order_amount_before_fee']
                record['top_up_commission'] = record['order_amount_before_fee'] * card['BP_RECHARGE_RATE']
                # record['top_up_channel_fee'] = record['order_amount_before_fee'] * card['BP_CHANNEL_RECHARGE_RATE']
                # record['top_up_as_commission'] = record['order_amount_before_fee'] * card['BP_AS_RECHARGE_RATE']
                # record['top_up_mw_commission'] = record['order_amount_before_fee'] * card['BP_MW_RECHARGE_RATE']
        elif 'EE' in record['card_issuer']:
            if is_apply:
                record['apply_amount'] = card['EE_APPLY_FEE']
                # record['apply_channel_fee'] = card['EE_CHANNEL_APPLY_FEE']
                # record['apply_as_commission'] = card['EE_AS_APPLY_FEE']
                # record['apply_mw_commission'] = card['EE_MW_APPLY_FEE']
                record['top_up_amount'] = card['EE_MIN_TOP_UP']
                record['top_up_commission'] = card['EE_MIN_TOP_UP'] * card['EE_RECHARGE_RATE']
                # record['top_up_channel_fee'] = card['EE_MIN_TOP_UP'] * card['EE_CHANNEL_RECHARGE_RATE']
                # record['top_up_as_commission'] = card['EE_MIN_TOP_UP'] * card['EE_AS_RECHARGE_RATE']
                # record['top_up_mw_commission'] = card['EE_MIN_TOP_UP'] * card['EE_MW_RECHARGE_RATE']
            else:
                record['top_up_amount'] = record['order_amount_before_fee']
                record['top_up_commission'] = record['order_amount_before_fee'] * card['EE_RECHARGE_RATE']
                # record['top_up_channel_fee'] = record['order_amount_before_fee'] * card['EE_CHANNEL_RECHARGE_RATE']
                # record['top_up_as_commission'] = record['order_amount_before_fee'] * card['EE_AS_RECHARGE_RATE']
                # record['top_up_mw_commission'] = record['order_amount_before_fee'] * card['EE_MW_RECHARGE_RATE']
        elif 'FO' in record['card_issuer']:
            if is_apply:
                record['apply_amount'] = card['FO_APPLY_FEE']
                # record['apply_channel_fee'] = card['FO_CHANNEL_APPLY_FEE']
                # record['apply_as_commission'] = card['FO_AS_APPLY_FEE']
                # record['apply_mw_commission'] = card['FO_MW_APPLY_FEE']
                record['top_up_amount'] = card['FO_MIN_TOP_UP']
                record['top_up_commission'] = card['FO_MIN_TOP_UP'] * card['FO_RECHARGE_RATE']
                # record['top_up_channel_fee'] = card['FO_MIN_TOP_UP'] * card['FO_CHANNEL_RECHARGE_RATE']
                # record['top_up_as_commission'] = card['FO_MIN_TOP_UP'] * card['FO_AS_RECHARGE_RATE']
                # record['top_up_mw_commission'] = card['FO_MIN_TOP_UP'] * card['FO_MW_RECHARGE_RATE']
            else:
                record['top_up_amount'] = record['order_amount_before_fee']
                record['top_up_commission'] = record['order_amount_before_fee'] * card['FO_RECHARGE_RATE']
                # record['top_up_channel_fee'] = record['order_amount_before_fee'] * card['FO_CHANNEL_RECHARGE_RATE']
                # record['top_up_as_commission'] = record['order_amount_before_fee'] * card['FO_AS_RECHARGE_RATE']
                # record['top_up_mw_commission'] = record['order_amount_before_fee'] * card['FO_MW_RECHARGE_RATE']

        record['overpaid_amount'] = record['paid_amount'] - record['order_amount_after_fee']

    return record


def _calculate_revenue(records, is_apply):
    if is_apply:
        records['apply_amount'] = None
        # records['apply_commission'] = None
    records['top_up_amount'] = None
    records['top_up_commission'] = None
    records['overpaid_amount'] = None

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
