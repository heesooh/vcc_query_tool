from .engine import *
from .sql import *

import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def get_payment_gateway_records(from_date, to_date):
    sql_engine = get_pg_engine()
    query_script = get_pg_query_script(from_date, to_date)

    try:
        with sql_engine.connect() as conn:
            return pd.read_sql_query(query_script, conn)

    except ConnectionError as e:
        print("Failed to connet to the remote server: ", e)
    except Exception as e:
        print("An unexpected error has occurred: ", e)


def get_card_records(from_date, to_date):
    tunnel = get_card_tunnel()

    try:
        tunnel.start()
        sql_engine = get_card_engine(tunnel.local_bind_port)
        query_script = get_card_query_script(from_date, to_date)

        with sql_engine.connect() as conn:
            card_records = pd.read_sql_query(query_script, conn)

    except ConnectionError as e:
        print("Failed to connet to the remote server: ", e)
    except Exception as e:
        print("An unexpected error has occurred: ", e)

    finally:
        tunnel.stop()
        return card_records
