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
    'table1': os.getenv('PAYMENT_GATEWAY_TABLE1'),
    'table2': os.getenv('PAYMENT_GATEWAY_TABLE2'),
    'password': os.getenv('PAYMENT_GATEWAY_PASSWORD'),
    'database': os.getenv('PAYMENT_GATEWAY_DB')
}

mw_card_server = {
    'ssh_host': os.getenv('SSH_HOSTNAME'),
    'ssh_user': os.getenv('SSH_USERNAME'),
    'ssh_pkey': os.getenv('SSH_KEY_PATH'),
    'ssh_port': int(os.getenv('SSH_PORT')),
    'sql_host': os.getenv('MYSQL_HOST'),
    'sql_user': os.getenv('MYSQL_USERNAME'),
    'sql_pass': os.getenv('MYSQL_PASSWORD'),
    'sql_port': int(os.getenv('MYSQL_PORT'))
}


def _get_payment_gateway_records(from_date, to_date):
    mysql_url = f"mysql+pymysql://{payment_gateway['user']}:{payment_gateway['password']}@" \
                f"{payment_gateway['host']}:{payment_gateway['port']}/{payment_gateway['database']}"

    sqlalchemy_engine = create_engine(mysql_url)

    query = text(f"""
        SELECT
            B.order_id,
            B.merchant_order_id,
            B.merchant_id,
            A.status AS udun_tx_status,
            B.order_status,
            B.amount,
            B.coin_id,
            B.address AS recipient_address,
            A.tx_id,
            B.create_time,
            B.update_time,
            B.paid_amount,
            B.refund_amount,
            B.pay_status,
            B.refund_time,
            B.expire_time,
            B.closed_time,
            B.notify_url,
            B.redirect_url
        FROM (
            SELECT *
            FROM {payment_gateway['table1']}
            WHERE DATE(create_time) BETWEEN :from_date AND :to_date) AS A
        INNER JOIN (
            SELECT *
            FROM {payment_gateway['table2']}
            WHERE DATE(closed_time) BETWEEN :from_date AND :to_date) AS B
        ON A.order_id = B.order_id
        ORDER BY A.create_time;
    """)

    with sqlalchemy_engine.connect() as conn:
        return pd.read_sql_query(query, conn, params={"from_date": from_date, "to_date": to_date})


def _get_mw_order_records(from_date, to_date):
    tunnel = SSHTunnelForwarder(
        (mw_card_server['ssh_host'], mw_card_server['ssh_port']),
        ssh_username=mw_card_server['ssh_user'],
        ssh_pkey=mw_card_server['ssh_pkey'],
        remote_bind_address=(mw_card_server['sql_host'], mw_card_server['sql_port'])
    )

    try:
        tunnel.start()
        local_port = tunnel.local_bind_port
        sqlalchemy_engine = create_engine(f"mysql+pymysql://{mw_card_server['sql_user']}:"
                                          f"{mw_card_server['sql_pass']}@localhost:{local_port}")

        query = text(f"""
            SELECT A.order_id, B.user_id, B.card_id, A.order_coin_id, A.order_amount_before_fee, A.order_amount_after_fee, A.order_data, A.order_type, A.order_timestamp, B.name_on_card, B.kyc_status, B.card_status, B.card_number, B.active_date, A.card_project, B.card_issuer
            FROM (
               SELECT id AS order_id, user_id, card_id, merchant_order_id, coin_id AS order_coin_id, base_amount AS order_amount_before_fee, amount_to_pay AS order_amount_after_fee, base_currency AS order_currency, order_data, order_type, timestamp AS order_timestamp, 'MW CARD' AS card_project
                FROM mw_card.airswift_order
                WHERE STR_TO_DATE(SUBSTRING(timestamp, 1, 8), '%Y%m%d') BETWEEN :from_date AND :to_date
            
                UNION ALL
            
                SELECT id AS order_id, user_id, card_id, merchant_order_id, coin_id AS order_coin_id, base_amount AS order_amount_before_fee, amount_to_pay AS order_amount_after_fee, base_currency AS order_currency, order_data, order_type, timestamp AS order_timestamp, 'U CARD' AS card_project
                FROM ucard.airswift_order
                WHERE STR_TO_DATE(SUBSTRING(timestamp, 1, 8), '%Y%m%d') BETWEEN :from_date AND :to_date
            
                UNION ALL
            
                SELECT id AS order_id, user_id, card_id, merchant_order_id, coin_id AS order_coin_id, base_amount AS order_amount_before_fee, amount_to_pay AS order_amount_after_fee, base_currency AS order_currency, order_data, order_type, timestamp AS order_timestamp, 'KIM CARD' AS card_project
                FROM kimcard.airswift_order
                WHERE STR_TO_DATE(SUBSTRING(timestamp, 1, 8), '%Y%m%d') BETWEEN :from_date AND :to_date
            
                UNION ALL
            
                SELECT id AS order_id, user_id, card_id, merchant_order_id, coin_id AS order_coin_id, base_amount AS order_amount_before_fee, amount_to_pay AS order_amount_after_fee, base_currency AS order_currency, order_data, order_type, timestamp AS order_timestamp, 'TON CARD' AS card_project
                FROM toncard.airswift_order
                WHERE STR_TO_DATE(SUBSTRING(timestamp, 1, 8), '%Y%m%d') BETWEEN :from_date AND :to_date
                 ) AS A
            LEFT JOIN (
                SELECT card_info.*, user_info.email, user_info.kyc_status
                FROM (
                    # ======================================
                    # Get Card Information (For Block Purse)
                    # ======================================
                    SELECT card.merchant_order_id, card.card_id, card.user_id, dashboard.name_on_card, dashboard.card_number, card.active_date, dashboard.status AS card_status, dashboard.balance, dashboard.currency, 'BP' AS card_issuer
                    FROM mw_card.blockpurse_card AS card
                    LEFT JOIN (
                        SELECT id, name_on_card, status, balance, currency, pan AS card_number
                        FROM mwcard_dashboard.card
                    ) AS dashboard
                    ON card.card_id = dashboard.id
                    
                    UNION ALL
                    
                    SELECT card.merchant_order_id, card.card_id, card.user_id, dashboard.name_on_card, dashboard.card_number, card.active_date, dashboard.status AS card_status, dashboard.balance, dashboard.currency, 'BP' AS card_issuer
                    FROM ucard.blockpurse_card AS card
                    LEFT JOIN (
                        SELECT id, name_on_card, status, balance, currency, pan AS card_number
                        FROM ucard_dashboard.card
                    ) AS dashboard
                    ON card.card_id = dashboard.id
                    
                    UNION ALL
                    
                    SELECT card.merchant_order_id, card.card_id, card.user_id, dashboard.name_on_card, dashboard.card_number, card.active_date, dashboard.status AS card_status, dashboard.balance, dashboard.currency, 'BP' AS card_issuer
                    FROM toncard.blockpurse_card AS card
                    LEFT JOIN (
                        SELECT id, name_on_card, status, balance, currency, pan AS card_number
                        FROM toncard_dashboard.card
                    ) AS dashboard
                    ON card.card_id = dashboard.id
                    
                    UNION ALL
                    
                    SELECT card.merchant_order_id, card.card_id, card.user_id, dashboard.name_on_card, dashboard.card_number, card.active_date, dashboard.status AS card_status, dashboard.balance, dashboard.currency, 'BP' AS card_issuer
                    FROM kimcard.blockpurse_card AS card
                    LEFT JOIN (
                        SELECT id, name_on_card, status, balance, currency, pan AS card_number
                        FROM kimcard_dashboard.card
                    ) AS dashboard
                    ON card.card_id = dashboard.id
            
                    UNION ALL
            
                    # ====================================
                    # Get Card Information (For Easy Euro)
                    # ====================================
                    SELECT card.merchant_order_id, card.id AS card_id, card.user_id, dashboard.name_on_card, dashboard.card_number, card.activation_date AS activate_date, dashboard.status AS card_status, dashboard.balance, dashboard.currency, 'EE' AS card_issuer
                    FROM mw_card.easyeuro_card AS card
                    LEFT JOIN (
                        SELECT id, name_on_card, status, balance, currency, pan AS card_number
                        FROM mwcard_dashboard.card
                    ) AS dashboard
                    ON card.id = dashboard.id
            
                    UNION ALL
                    
                    SELECT card.merchant_order_id, card.id AS card_id, card.user_id, dashboard.name_on_card, dashboard.card_number, card.activation_date AS activate_date, dashboard.status AS card_status, dashboard.balance, dashboard.currency, 'EE' AS card_issuer
                    FROM ucard.easyeuro_card AS card
                    LEFT JOIN (
                        SELECT id, name_on_card, status, balance, currency, pan AS card_number
                        FROM ucard_dashboard.card
                    ) AS dashboard
                    ON card.id = dashboard.id
            
                    UNION ALL
                    
                    SELECT card.merchant_order_id, card.id AS card_id, card.user_id, dashboard.name_on_card, dashboard.card_number, card.activation_date AS activate_date, dashboard.status AS card_status, dashboard.balance, dashboard.currency, 'EE' AS card_issuer
                    FROM kimcard.easyeuro_card AS card
                    LEFT JOIN (
                        SELECT id, name_on_card, status, balance, currency, pan AS card_number
                        FROM kimcard_dashboard.card
                    ) AS dashboard
                    ON card.id = dashboard.id
            
                    UNION ALL
            
                    # ========================================
                    # Get Card Information (For Financial One)
                    # ========================================
                    SELECT card.merchant_order_id, card.id AS card_id, card.user_id, dashboard.name_on_card, dashboard.card_number, card.activation_date AS activate_date, dashboard.status AS card_status, dashboard.balance, dashboard.currency, 'FO' AS card_issuer
                    FROM mw_card.financial_one_card AS card
                    LEFT JOIN (
                        SELECT id, name_on_card, status, balance, currency, pan AS card_number
                        FROM mwcard_dashboard.card
                    ) AS dashboard
                    ON card.id = dashboard.id
                    
                    UNION  ALL 
                    
                    SELECT card.merchant_order_id, card.id AS card_id, card.user_id, dashboard.name_on_card, dashboard.card_number, card.activation_date AS activate_date, dashboard.status AS card_status, dashboard.balance, dashboard.currency, 'FO' AS card_issuer
                    FROM ucard.financial_one_card AS card
                    LEFT JOIN (
                        SELECT id, name_on_card, status, balance, currency, pan AS card_number
                        FROM ucard_dashboard.card
                    ) AS dashboard
                    ON card.id = dashboard.id
                    
                    UNION  ALL  
                
                    SELECT card.merchant_order_id, card.id AS card_id, card.user_id, dashboard.name_on_card, dashboard.card_number, card.activation_date AS activate_date, dashboard.status AS card_status, dashboard.balance, dashboard.currency, 'FO' AS card_issuer
                    FROM kimcard.financial_one_card AS card
                    LEFT JOIN (
                        SELECT id, name_on_card, status, balance, currency, pan AS card_number
                        FROM kimcard_dashboard.card
                    ) AS dashboard
                    ON card.id = dashboard.id
                ) AS card_info
                LEFT JOIN (
                    # Get User Information (ALL MW Projects)
                    SELECT uid AS user_id, email, kyc_status
                    FROM card_user.Users
                ) AS user_info
                ON card_info.user_id = user_info.user_id
            ) AS B
            ON (A.merchant_order_id = B.merchant_order_id OR A.card_id = B.card_id);
        """)

        with sqlalchemy_engine.connect() as conn:
            mw_order_records = pd.read_sql_query(query, conn, params={"from_date": from_date, "to_date": to_date})

    finally:
        tunnel.stop()
        return mw_order_records


def _merge_records(payment_records, order_records):
    order_records['order_id'] = pd.to_numeric(order_records['order_id'], errors='coerce').astype('int64')
    merge_records = pd.merge(payment_records, order_records, how='left', on='order_id')

    return merge_records


def get_records(from_date, to_date):
    payment_records = _get_payment_gateway_records(from_date, to_date)
    order_records = _get_mw_order_records(from_date, to_date)
    query_result = _merge_records(payment_records, order_records)

    return query_result


def _get_monthly_fee_cards(active_cards, input_date):
    input_date = datetime.strptime(input_date, '%Y-%m-%d')
    fee_before_date = datetime(input_date.year, input_date.month, 16)
    timestamp = datetime.timestamp(fee_before_date)

    monthly_fee_cards_1 = active_cards[active_cards['active_date'] < timestamp]
    monthly_fee_cards_2 = monthly_fee_cards_1[monthly_fee_cards_1['merchant_order_id'] != 'FROM_VOUCHER']

    return monthly_fee_cards_2


def _get_active_cards():
    mysql_url = f"mysql+pymysql://{mw_card_server['user']}:{mw_card_server['password']}@" \
                f"{mw_card_server['host']}:{mw_card_server['port']}"

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
