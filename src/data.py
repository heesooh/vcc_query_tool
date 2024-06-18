import os
from dotenv import load_dotenv

import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()

# Payment Gateway
payment_gateway = {
    'host': os.getenv('PAYMENT_GATEWAY_HOST'),
    'port': int(os.getenv('PAYMENT_GATEWAY_PORT')),
    'user': os.getenv('PAYMENT_GATEWAY_USER'),
    'password': os.getenv('PAYMENT_GATEWAY_PASSWORD'),
    'database': os.getenv('PAYMENT_GATEWAY_DB'),
    'table1': os.getenv('PAYMENT_GATEWAY_TABLE1'),
    'table2': os.getenv('PAYMENT_GATEWAY_TABLE2')
}

card_server = {
    'host': os.getenv('CARD_HOST'),
    'port': int(os.getenv('CARD_PORT')),
    'user': os.getenv('CARD_USER'),
    'password': os.getenv('CARD_PASSWORD'),
}


def _payment_records(from_date, to_date):
    mysql_url = f"mysql+pymysql://{payment_gateway['user']}:{payment_gateway['password']}@" \
                f"{payment_gateway['host']}:{payment_gateway['port']}/{payment_gateway['database']}"

    sqlalchemy_engine = create_engine(mysql_url)

    query = text(f"""
        SELECT
            r.tx_id,
            r.order_id,
            r.address as recipient_address,
            o.amount as requested_amount,
            r.amount as paid_amount,
            r.coin_id,
            o.pay_status,
            o.merchant_id,
            o.merchant_order_id,
            r.create_time
        FROM (
            SELECT *
            FROM {payment_gateway['table1']} r
            WHERE DATE(create_time) BETWEEN :from_date AND :to_date) AS r
        LEFT JOIN (
            SELECT *
            FROM {payment_gateway['table2']} r
            WHERE DATE(closed_time) BETWEEN :from_date AND :to_date) AS o
        ON r.order_id = o.order_id
        ORDER BY r.create_time
    """)

    with sqlalchemy_engine.connect() as conn:
        return pd.read_sql_query(query, conn, params={"from_date": from_date, "to_date": to_date})


def _order_records(from_date, to_date):
    mysql_url = f"mysql+pymysql://{card_server['user']}:{card_server['password']}@" \
                f"{card_server['host']}:{card_server['port']}"

    sqlalchemy_engine = create_engine(mysql_url)

    db_list = ['mw_card', 'ucard', 'toncard']
    dfs = []

    for db in db_list:
        query = text(f"""
            SELECT ab.*, u.email, u.kyc_status
            FROM (
                SELECT *
                FROM card_user.Users 
                WHERE kyc_status = 'PASSED'
            ) AS u
            RIGHT JOIN (
                SELECT
                    a.id as order_id,
                    a.user_id,
                    a.coin_id,
                    a.merchant_order_id,
                    a.timestamp,
                    a.base_amount,
                    a.base_currency,
                    a.amount_to_pay,
                    a.order_data,
                    a.order_type,
                    a.status AS order_status,
                    b.card_id,
                    b.alias,
                    b.card_no,
                    b.cvv,
                    b.balance,
                    b.status AS card_status,
                    b.currency
                FROM (
                    SELECT *
                    FROM {db}.airswift_order
                    WHERE status = 'SUCCESS'
                    AND STR_TO_DATE(SUBSTRING(timestamp, 1, 8), '%Y%m%d') BETWEEN :from_date AND :to_date
                ) AS a
                LEFT JOIN {db}.blockpurse_card AS b 
                ON b.merchant_order_id = a.merchant_order_id
            ) AS ab 
            ON u.uid = ab.user_id
        """)

        with sqlalchemy_engine.connect() as conn:
            df = pd.read_sql_query(query, conn, params={"from_date": from_date, "to_date": to_date})
            df['card_name'] = db
            dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def _merge_records(payment_record, order_record):
    order_record['order_id'] = pd.to_numeric(order_record['order_id'], errors='coerce').astype('int64')
    merged_records = pd.merge(payment_record, order_record, how='left', on='order_id')

    return merged_records


def get_records(from_date, to_date):
    payment_df = _payment_records(from_date, to_date)
    order_df = _order_records(from_date, to_date)
    merged_df = _merge_records(payment_df, order_df)

    return merged_df


def get_pending_records(order_ids):
    mysql_url = f"mysql+pymysql://{card_server['user']}:{card_server['password']}@" \
                f"{card_server['host']}:{card_server['port']}"

    sqlalchemy_engine = create_engine(mysql_url)

    order_ids_str = ', '.join(f"'{id}'" for id in order_ids if id)

    db_list = ['mw_card', 'ucard', 'toncard']
    dfs = []

    for db in db_list:
        query = text(f"""
            SELECT ab.*, u.email, u.kyc_status
            FROM (
                SELECT *
                FROM card_user.Users 
                WHERE kyc_status = 'PASSED'
            ) AS u
            RIGHT JOIN (
                SELECT
                    a.id as order_id,
                    a.user_id,
                    a.coin_id,
                    a.merchant_order_id,
                    a.timestamp,
                    a.base_amount,
                    a.base_currency,
                    a.amount_to_pay,
                    a.order_data,
                    a.order_type,
                    a.status AS order_status,
                    b.card_id,
                    b.alias,
                    b.card_no,
                    b.cvv,
                    b.balance,
                    b.status AS card_status,
                    b.currency
                FROM (
                    SELECT *
                    FROM {db}.airswift_order
                    WHERE id IN (
                        {order_ids_str}
                    )
                ) AS a
                LEFT JOIN {db}.blockpurse_card AS b 
                ON b.merchant_order_id = a.merchant_order_id
            ) AS ab 
            ON u.uid = ab.user_id
        """)

        with sqlalchemy_engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
            df['card_name'] = db
            dfs.append(df)

    non_empty_dfs = [df.dropna(axis=1, how='all') for df in dfs]

    return pd.concat(non_empty_dfs, ignore_index=True)

