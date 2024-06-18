import os
from archive.sql import *
from dotenv import load_dotenv

load_dotenv()

# Payment Gateway
PAYMENT_GATEWAY_HOST = os.getenv('PAYMENT_GATEWAY_HOST')
PAYMENT_GATEWAY_PORT = os.getenv('PAYMENT_GATEWAY_PORT')
PAYMENT_GATEWAY_DB = os.getenv('PAYMENT_GATEWAY_DB')
PAYMENT_GATEWAY_USER = os.getenv('PAYMENT_GATEWAY_USER')
PAYMENT_GATEWAY_PASSWORD = os.getenv('PAYMENT_GATEWAY_PASSWORD')
PAYMENT_GATEWAY_TABLE1 = os.getenv('PAYMENT_GATEWAY_TABLE1')
PAYMENT_GATEWAY_TABLE2 = os.getenv('PAYMENT_GATEWAY_TABLE2')

PAYMENT_GATEWAY_CONFIG = {
    'host': PAYMENT_GATEWAY_HOST,
    'port': int(PAYMENT_GATEWAY_PORT),
    'database': PAYMENT_GATEWAY_DB,
    'user': PAYMENT_GATEWAY_USER,
    'password': PAYMENT_GATEWAY_PASSWORD,
}

# Card Database
CARD_HOST = os.getenv('CARD_HOST')
CARD_PORT = os.getenv('CARD_PORT')
CARD_USER = os.getenv('CARD_USER')
CARD_PASSWORD = os.getenv('CARD_PASSWORD')

CARD_CONFIG = {
    'host': CARD_HOST,
    'port': int(CARD_PORT),
    'user': CARD_USER,
    'password': CARD_PASSWORD,
}


def payment_records(from_date, to_date):
    connect = mysql_connect(PAYMENT_GATEWAY_CONFIG)
    query = (f"""
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
            FROM {PAYMENT_GATEWAY_TABLE1}
            WHERE create_time >= %s AND create_time <= %s) AS r
        LEFT JOIN (
            SELECT *
            FROM {PAYMENT_GATEWAY_TABLE2}
            WHERE closed_time >= %s AND closed_time <= %s) AS o
        ON r.order_id = o.order_id
        ORDER BY r.create_time
    """)
    result = mysql_query(connect, query, (from_date, to_date, from_date, to_date))
    print(type(result))
    mysql_disconnect(connect)


# payment_records('2024-05-01', '2025-05-31')


def card_records():
    db_list = ['mw_card', 'ucard', 'toncard']
    connect = mysql_connect(CARD_CONFIG)
    for db in db_list:
        print(("\nQuerying to database: " + db + ".....\n").upper())

        query = f"""
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
                    AND timestamp LIKE '202405%'
                ) AS a
                LEFT JOIN {db}.blockpurse_card AS b 
                ON b.merchant_order_id = a.merchant_order_id
            ) AS ab 
            ON u.uid = ab.user_id
        """

        result = mysql_query(connect, query, None)
        print(type(result))

    mysql_disconnect(connect)


card_records()
