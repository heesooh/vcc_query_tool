import os
from dotenv import load_dotenv
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text
from sshtunnel import SSHTunnelForwarder

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

load_dotenv()

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
    'ssh_host': os.getenv('SSH_HOSTNAME'),
    'ssh_user': os.getenv('SSH_USERNAME'),
    'ssh_pkey': os.getenv('SSH_KEY_PATH'),
    'ssh_port': int(os.getenv('SSH_PORT')),
    'vcc_host': os.getenv('MYSQL_HOST'),
    'vcc_user': os.getenv('MYSQL_USERNAME'),
    'vcc_pass': os.getenv('MYSQL_PASSWORD'),
    'vcc_port': int(os.getenv('MYSQL_PORT'))
}


def _payment_records(from_date, to_date):
    mysql_url = f"mysql+pymysql://{payment_gateway['user']}:{payment_gateway['password']}@" \
                f"{payment_gateway['host']}:{payment_gateway['port']}/{payment_gateway['database']}"

    sqlalchemy_engine = create_engine(mysql_url)

    query = text(f"""
        SELECT
            r.create_time as order_time,
            r.order_id,
            r.tx_id as transaction_hash,
            r.address as receiver_address,
            o.pay_status,
            o.amount as order_amount,
            r.amount as paid_amount,
            r.coin_id as order_currency
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
    order_records = []

    tunnel = SSHTunnelForwarder(
        (card_server['ssh_host'], card_server['ssh_port']),
        ssh_username=card_server['ssh_user'],
        ssh_pkey=card_server['ssh_pkey'],
        remote_bind_address=(card_server['vcc_host'], card_server['vcc_port'])
    )

    try:
        tunnel.start()

        local_port = tunnel.local_bind_port

        sqlalchemy_engine = create_engine(f"mysql+pymysql://{card_server['vcc_user']}:{card_server['vcc_pass']}@localhost:{local_port}")

        db_list = ['mw_card', 'ucard', 'toncard']

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
                        a.merchant_order_id,
                        a.base_amount,
                        a.order_data,
                        a.order_type,
                        a.status AS order_status,
                        a.card_id as order_card_id,
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
                    ON (b.merchant_order_id = a.merchant_order_id OR b.card_id = a.card_id)
                ) AS ab 
                ON u.uid = ab.user_id
            """)

            with sqlalchemy_engine.connect() as conn:
                df = pd.read_sql_query(query, conn, params={"from_date": from_date, "to_date": to_date})
                df['card_name'] = db
                order_records.append(df)

    finally:
        tunnel.stop()
        return pd.concat(order_records, ignore_index=True)


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
    pending_records = []

    tunnel = SSHTunnelForwarder(
        (card_server['ssh_host'], card_server['ssh_port']),
        ssh_username=card_server['ssh_user'],
        ssh_pkey=card_server['ssh_pkey'],
        remote_bind_address=(card_server['vcc_host'], card_server['vcc_port'])
    )

    try:
        tunnel.start()

        local_port = tunnel.local_bind_port
        order_ids_str = ', '.join(f"'{id}'" for id in order_ids if id)

        sqlalchemy_engine = create_engine(f"mysql+pymysql://{card_server['vcc_user']}:{card_server['vcc_pass']}@localhost:{local_port}")

        db_list = ['mw_card', 'ucard', 'toncard']

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
                        a.card_id as order_card_id,
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
                    ON (b.merchant_order_id = a.merchant_order_id OR b.card_id = a.card_id)
                ) AS ab 
                ON u.uid = ab.user_id
            """)

            with sqlalchemy_engine.connect() as conn:
                df = pd.read_sql_query(query, conn)
                df['card_name'] = db
                pending_records.append(df)

    finally:
        tunnel.stop()
        non_empty_pending_records = [df.dropna(axis=1, how='all') for df in pending_records]
        return pd.concat(non_empty_pending_records, ignore_index=True)


def _get_monthly_fee_cards(active_cards, input_date):
    input_date = datetime.strptime(input_date, '%Y-%m-%d')
    fee_before_date = datetime(input_date.year, input_date.month, 16)
    timestamp = datetime.timestamp(fee_before_date)

    monthly_fee_cards_1 = active_cards[active_cards['active_date'] < timestamp]
    monthly_fee_cards_2 = monthly_fee_cards_1[monthly_fee_cards_1['merchant_order_id'] != 'FROM_VOUCHER']

    return monthly_fee_cards_2


def _get_active_cards():
    mysql_url = f"mysql+pymysql://{card_server['user']}:{card_server['password']}@" \
                f"{card_server['host']}:{card_server['port']}"

    sqlalchemy_engine = create_engine(mysql_url)

    db_list = ['mw_card', 'ucard', 'toncard']
    dfs = []

    for db in db_list:
        query = text(f"""
            SELECT *
            FROM {db}.blockpurse_card AS bc
            WHERE status = "NORMAL" 
            AND user_id NOT IN (
                '573e68a0-1fc1-4563-a0f7-17389279c1ba',
                'fb31757d-b679-4e61-b433-ee6c1e8de365',
                '49e7c755-d649-4efc-a39c-5c2803f8486d',
                'f7c06b6b-9d7b-4e2c-8ead-18658ac0fdcf')
        """)

        with sqlalchemy_engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
            df['card_name'] = db
            dfs.append(df)

    non_empty_dfs = [df.dropna(axis=1, how='all') for df in dfs]

    return pd.concat(non_empty_dfs, ignore_index=True)
