import os

from dotenv import load_dotenv

load_dotenv('../../credentials/.env')


def get_payment_gateway_config():
    return {
        'host': os.getenv('PAYMENT_GATEWAY_HOST'),
        'port': int(os.getenv('PAYMENT_GATEWAY_PORT')),

        'user': os.getenv('PAYMENT_GATEWAY_USER'),
        'password': os.getenv('PAYMENT_GATEWAY_PASSWORD'),
    }


def get_payment_gateway_db_config():
    return {
        'db': os.getenv('PAYMENT_GATEWAY_DB'),

        'table1': os.getenv('PAYMENT_GATEWAY_TABLE1'),
        'table2': os.getenv('PAYMENT_GATEWAY_TABLE2')
    }


def get_card_tunnel_config():
    return {
        'host': os.getenv('CARD_TUNNEL_HOSTNAME'),
        'port': int(os.getenv('CARD_TUNNEL_PORT')),

        'user': os.getenv('CARD_TUNNEL_USERNAME'),
        'password': os.getenv('CARD_TUNNEL_KEY_PATH'),
    }


def get_card_config():
    return {
        'host': os.getenv('CARD_HOST'),
        'port': int(os.getenv('CARD_PORT')),

        'user': os.getenv('CARD_USERNAME'),
        'password': os.getenv('CARD_PASSWORD'),
    }


def get_card_db_config():
    return {
        'db00': os.getenv('CARD_DB00'),
        'db11': os.getenv('CARD_DB11'),
        'db12': os.getenv('CARD_DB12'),
        'db21': os.getenv('CARD_DB21'),
        'db22': os.getenv('CARD_DB22'),
        'db31': os.getenv('CARD_DB31'),
        'db32': os.getenv('CARD_DB32'),

        'table1': os.getenv('CARD_TABLE1'),
        'table2': os.getenv('CARD_TABLE2'),
        'table3': os.getenv('CARD_TABLE3'),
        'table4': os.getenv('CARD_TABLE4'),
    }


def get_internal_address():
    return {
        'test_account_1': os.getenv('INTERNAL_ADDRESS_1'),
        'test_account_2': os.getenv('INTERNAL_ADDRESS_2'),
        'test_account_3': os.getenv('INTERNAL_ADDRESS_3'),
        'test_account_4': os.getenv('INTERNAL_ADDRESS_4'),
        'test_account_5': os.getenv('INTERNAL_ADDRESS_5'),
        'test_account_6': os.getenv('INTERNAL_ADDRESS_6'),
        'test_account_7': os.getenv('INTERNAL_ADDRESS_7')
    }


def get_google_sheet_config():
    return {
        'id': os.getenv('GOOGLE_SHEET_ID')
    }
