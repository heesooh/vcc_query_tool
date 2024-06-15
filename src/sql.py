import mysql.connector
from mysql.connector import Error


def mysql_connect(config):
    connect = None
    try:
        connect = mysql.connector.connect(**config)
        if connect.is_connected():
            print("Connected to MySQL Server version ", connect.get_server_info())
        else:
            print("Failed to connect to MySQL")
    except Error as e:
        print(e)
    finally:
        if not connect.is_connected() and connect is not None:
            connect.close()
            print("MySQL connection is closed")
    return connect


def mysql_disconnect(connect):
    try:
        if connect.is_connected():
            connect.close()
            print("Disconnected from MySQL")
            return True
        else:
            print("Already disconnected from MySQL")
    except Error as e:
        print(e)

    return False


def mysql_query(connect, sql_query, args=None):
    cursor = connect.cursor()
    cursor.execute(sql_query, args)
    # TODO: Replace with 'return cursor.fetchall()' later
    query_result = cursor.fetchall()
    for row in query_result:
        print(row)
    return query_result
