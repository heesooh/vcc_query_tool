import os
import csv
from scraper import *
from dotenv import load_dotenv

load_dotenv()
test_account_1 = os.getenv('INTERNAL_ADDRESS_1')
test_account_2 = os.getenv('INTERNAL_ADDRESS_2')
test_account_3 = os.getenv('INTERNAL_ADDRESS_3')
test_account_4 = os.getenv('INTERNAL_ADDRESS_4')
test_account_5 = os.getenv('INTERNAL_ADDRESS_5')
write_file_name = os.getenv('WRITE_FILE_NAME')
read_file_name = os.getenv('READ_FILE_NAME')
db_table_name = os.getenv('DB_TABLE_NAME')


def is_erc_address(address):
    return address.startswith('0x')


def is_test_address(address):
    test_addresses = [
        test_account_1,
        test_account_2,
        test_account_3,
        test_account_4,
        test_account_5
    ]

    return address in test_addresses


def get_sender_address(row):
    sender_address = ''
    record = []

    if is_erc_address(row[5]):
        sender_address = get_erc_sender_address(row[0])
    else:
        sender_address = get_trc_sender_address(row[0])

    if is_test_address(sender_address):
        record.append('Test Transaction')
    else:
        record.append('Client Transaction')

    record.extend(row[0:2])
    record.append(sender_address)
    record.extend(row[5:10])

    return record


def csv_builder(data):
    print("Creating New CSV File...")

    with open(write_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("New CSV data successfully created!")


def csv_reader():
    data = [['tx_type', 'tx_hash', 'order_id', 'sender', 'receiver', 'transaction_amount', 'currency', 'create_time',
             'update_time']]  # csv write data

    with open(read_file_name, 'r') as payment_record:
        reader = csv.reader(payment_record)
        next(reader)

        for row in reader:
            data.append(get_sender_address(row))

    return data


csv_data = csv_reader()
csv_builder(csv_data)


def query_builder():
    with open(write_file_name, 'r') as payment_record:
        reader = csv.reader(payment_record)
        next(reader)

        query = 'SELECT *\nFROM ' + db_table_name + '\nWHERE id IN ('

        for row in reader:
            tx_type = row[0]
            order_id = row[2]
            if tx_type == 'Client Transaction':
                query += "'" + order_id + "', "
        query = query[:-2] + ");"
        print(query)


query_builder()
