import os
import csv
import json
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
test_account_1 = os.getenv('INTERNAL_ADDRESS_1')
test_account_2 = os.getenv('INTERNAL_ADDRESS_2')
test_account_3 = os.getenv('INTERNAL_ADDRESS_3')
test_account_4 = os.getenv('INTERNAL_ADDRESS_4')
write_file_name = os.getenv('WRITE_FILE_NAME')
read_file_name = os.getenv('READ_FILE_NAME')
db_table_name = os.getenv('DB_TABLE_NAME')

def isERC20(address):
    return address.startswith('0x')

def getERCSenderAddress(txHash):
    url = 'https://etherscan.io/tx/' + txHash

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}
    try:
        time.sleep(0.5)
        response = requests.get(url, headers=headers)

        if (response.status_code == 200):
            soup = BeautifulSoup(response.text, 'html.parser')
            address_div = soup.select_one('div.col-md-9 > div > span > a[data-highlight-value]')
            if address_div:
                sender_address = address_div.text
                print("ERC20 Sender address: " + sender_address)
                return (sender_address)
            else:
                print("Sender's address not found.")
        else:
            print("Failed to Retrieve Data From: " + url)
    except requests.Timeout:
        print("Request time out!!")
    except requests.RequestException as error:
        print(f'An unexpected error occured: {str(error)}')

    return 'Not Found'

def getTRCSenderAddress(txHash):
    url = 'https://apilist.tronscanapi.com/api/transaction-info?hash=' + txHash
    
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"}

    try:
        time.sleep(0.5) # Delay request to address rate limit issue
        response = requests.get(url, headers=headers)

        if (response.status_code == 200):
            data = json.loads(response.text)
            if not data: 
                print("No Data Found!!")
            else: 
                print("TRC20 Sender address: " + data['ownerAddress'])
                return data['ownerAddress']
        else:
            print("Failed to Retrieve Data From: https://tronscan.org/#/transaction/" + txHash)
    except requests.Timeout:
        print("Request time out!!")
    except requests.RequestException as error:
        print(f'An unexpected error occured: {str(error)}')
    
    return 'Not Found'
    
def isTestAddress(address):
    test_addresses = [
        test_account_1,
        test_account_2,
        test_account_3,
        test_account_4
    ]
    
    return address in test_addresses

def recordBuilder(row):
    sender_address = ''
    record = []

    if (isERC20(row[5])):
        sender_address = getERCSenderAddress(row[0])        
    else:
        sender_address = getTRCSenderAddress(row[0])
    
    if (isTestAddress(sender_address)):
        record.append('Test Transaction')
    else:
        record.append('Client Transaction')
    
    record.extend(row[0:2])
    record.append(sender_address)
    record.extend(row[5:10])

    return record

def csvBuilder(data):
    print("Creating New CSV File...")

    with open(write_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("New CSV data successfully created!")
    
def txDataScraper():
    data = [['tx_type', 'tx_hash', 'order_id', 'sender', 'receiver', 'transaction_amount', 'currency', 'create_time', 'update_time']] # csv write data

    with open(read_file_name, 'r') as payment_record:
        reader = csv.reader(payment_record)
        next(reader)

        for row in reader:
            data.append(recordBuilder(row))

    csvBuilder(data)

def queryBuilder():
    with open(write_file_name, 'r') as payment_record:
        reader = csv.reader(payment_record)
        next(reader)

        query = 'SELECT *\nFROM ' + db_table_name + '\nWHERE id IN ('

        for row in reader:
            tx_type = row[0]
            order_id = row[2]
            if (tx_type == 'Client Transaction'):
                query += "'" + order_id + "', "
        query = query[:-2] + ");"
        print(query)

txDataScraper()
queryBuilder()