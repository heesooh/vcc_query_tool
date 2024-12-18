from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
from config import get_payment_gateway_config, get_payment_gateway_db_config, get_card_tunnel_config, get_card_config


def get_pg_engine():
    server = get_payment_gateway_config()
    database = get_payment_gateway_db_config()

    mysql_url = (f"mysql+pymysql://{server['user']}:{server['password']}@"
                 f"{server['host']}:{server['port']}/{database['db']}")

    return create_engine(mysql_url)


def get_card_tunnel():
    server = get_card_tunnel_config()
    database = get_card_config()

    return SSHTunnelForwarder(
        (server['host'], server['port']),
        ssh_username=server['user'],
        ssh_pkey=server['password'],
        remote_bind_address=(database['host'], database['port'])
    )


def get_card_engine(tunnel_bind_port):
    database = get_card_config()

    return create_engine(f"mysql+pymysql://{database['user']}:"
                         f"{database['password']}@localhost:{tunnel_bind_port}")
