from config import get_payment_gateway_db_config, get_card_db_config


def get_pg_query_script(from_date, to_date):
    config = get_payment_gateway_db_config()

    return f"""
        SELECT
            ORDER_CLOSED.order_id,
            ORDER_CLOSED.merchant_order_id,
            ORDER_CLOSED.merchant_id,
            PAYMENT_RECORD.status AS udun_tx_status,
            ORDER_CLOSED.order_status,
            ORDER_CLOSED.amount,
            ORDER_CLOSED.coin_id,
            ORDER_CLOSED.address AS recipient_address,
            PAYMENT_RECORD.tx_id,
            ORDER_CLOSED.create_time,
            ORDER_CLOSED.update_time,
            ORDER_CLOSED.paid_amount,
            ORDER_CLOSED.refund_amount,
            ORDER_CLOSED.pay_status,
            ORDER_CLOSED.refund_time,
            ORDER_CLOSED.expire_time,
            ORDER_CLOSED.closed_time,
            ORDER_CLOSED.notify_url,
            ORDER_CLOSED.redirect_url
        FROM (
            SELECT *
            FROM {config['table1']}
            WHERE DATE(create_time) BETWEEN '{from_date}' AND '{to_date}') AS PAYMENT_RECORD
        INNER JOIN (
            SELECT *
            FROM {config['table2']}
            WHERE DATE(closed_time) BETWEEN '{from_date}' AND '{to_date}') AS ORDER_CLOSED
        ON PAYMENT_RECORD.order_id = ORDER_CLOSED.order_id
        ORDER BY PAYMENT_RECORD.create_time;
    """


def get_card_query_script(from_date, to_date):
    config = get_card_db_config()

    return f"""  
        SELECT  
            ORDER_INFO.order_id,  
            CARD_INFO.user_id,  
            CARD_INFO.card_id,  
            ORDER_INFO.order_coin_id,  
            ORDER_INFO.order_amount_before_fee,  
            ORDER_INFO.order_amount_after_fee,  
            ORDER_INFO.order_data,  
            ORDER_INFO.order_type,  
            ORDER_INFO.order_timestamp,  
            CARD_INFO.name_on_card,  
            CARD_INFO.kyc_status,  
            CARD_INFO.card_status,  
            CARD_INFO.card_number,  
            CARD_INFO.activate_date,  
            ORDER_INFO.card_project,  
            CARD_INFO.card_issuer  
        FROM (  
            SELECT   
                id AS order_id,   
                user_id,   
                card_id,   
                merchant_order_id,   
                coin_id AS order_coin_id,   
                base_amount AS order_amount_before_fee,   
                amount_to_pay AS order_amount_after_fee,   
                base_currency AS order_currency,   
                order_data,   
                order_type,   
                timestamp AS order_timestamp,   
                'MW CARD' AS card_project  
            FROM {config['db11']}.{config['table1']}  
            WHERE STR_TO_DATE(SUBSTRING(timestamp, 1, 8), '%%Y%%m%%d') BETWEEN '{from_date}' AND '{to_date}'  
        
            UNION ALL  
        
            SELECT   
                id AS order_id,  
                user_id,  
                card_id,  
                merchant_order_id,  
                coin_id AS order_coin_id,  
                base_amount AS order_amount_before_fee,  
                amount_to_pay AS order_amount_after_fee,  
                base_currency AS order_currency,  
                order_data,  
                order_type,  
                timestamp AS order_timestamp,  
                'U CARD' AS card_project  
            FROM {config['db21']}.{config['table1']}  
            WHERE STR_TO_DATE(SUBSTRING(timestamp, 1, 8), '%%Y%%m%%d') BETWEEN '{from_date}' AND '{to_date}'  
        
            UNION ALL  
        
            SELECT   
                id AS order_id,  
                user_id,  
                card_id,  
                merchant_order_id,  
                coin_id AS order_coin_id,  
                base_amount AS order_amount_before_fee,  
                amount_to_pay AS order_amount_after_fee,  
                base_currency AS order_currency,  
                order_data,  
                order_type,  
                timestamp AS order_timestamp,  
                'KIM CARD' AS card_project  
            FROM {config['db31']}.{config['table1']}  
            WHERE STR_TO_DATE(SUBSTRING(timestamp, 1, 8), '%%Y%%m%%d') BETWEEN '{from_date}' AND '{to_date}'  
        ) AS ORDER_INFO  
        LEFT JOIN (  
            SELECT   
                FO_CARD_INFO.*,  
                ALL_USER_INFO.email,  
                ALL_USER_INFO.kyc_status  
            FROM (  
                SELECT   
                    card.merchant_order_id,  
                    card.id AS card_id,  
                    card.user_id,  
                    dashboard.name_on_card,  
                    dashboard.card_number,  
                    card.activation_date AS activate_date,  
                    dashboard.status AS card_status,  
                    dashboard.balance,  
                    dashboard.currency,  
                    'FO' AS card_issuer  
                FROM {config['db11']}.{config['table2']} AS card  
                LEFT JOIN (  
                    SELECT   
                        id,  
                        name_on_card,  
                        status,  
                        balance,  
                        currency,  
                        pan AS card_number  
                    FROM {config['db12']}.{config['table3']}  
                ) AS dashboard  
                ON card.id = dashboard.id  
        
                UNION  ALL  
        
                SELECT   
                    card.merchant_order_id,  
                    card.id AS card_id,  
                    card.user_id,  
                    dashboard.name_on_card,  
                    dashboard.card_number,  
                    card.activation_date AS activate_date,  
                    dashboard.status AS card_status,  
                    dashboard.balance,  
                    dashboard.currency,  
                    'FO' AS card_issuer  
                FROM {config['db21']}.{config['table2']} AS card  
                LEFT JOIN (  
                    SELECT   
                        id,  
                        name_on_card,  
                        status,  
                        balance,  
                        currency,  
                        pan AS card_number  
                    FROM {config['db22']}.{config['table3']}  
                ) AS dashboard  
                ON card.id = dashboard.id  
        
                UNION  ALL  
        
                SELECT   
                    card.merchant_order_id,  
                    card.id AS card_id,  
                    card.user_id,  
                    dashboard.name_on_card,  
                    dashboard.card_number,  
                    card.activation_date AS activate_date,  
                    dashboard.status AS card_status,  
                    dashboard.balance,  
                    dashboard.currency,  
                    'FO' AS card_issuer  
                FROM {config['db31']}.{config['table2']} AS card  
                LEFT JOIN (  
                    SELECT   
                        id,  
                        name_on_card,  
                        status,  
                        balance,  
                        currency,  
                        pan AS card_number  
                    FROM {config['db32']}.{config['table3']}  
                ) AS dashboard  
                ON card.id = dashboard.id  
            ) AS FO_CARD_INFO  
            LEFT JOIN (  
                SELECT   
                    uid AS user_id,  
                    email,  
                    kyc_status  
                FROM {config['db00']}.{config['table4']}  
            ) AS ALL_USER_INFO  
            ON FO_CARD_INFO.user_id = ALL_USER_INFO.user_id  
        ) AS CARD_INFO  
        ON (ORDER_INFO.merchant_order_id = CARD_INFO.merchant_order_id OR ORDER_INFO.card_id = CARD_INFO.card_id);  
    """
