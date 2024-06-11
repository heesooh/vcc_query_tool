import os
from sql import *
from dotenv import load_dotenv

load_dotenv()
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
    mysql_query(connect, query, (from_date, to_date, from_date, to_date))
    mysql_disconnect(connect)


payment_records('2024-06-01', '2025-06-30')
