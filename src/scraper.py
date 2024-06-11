import json
import time
import requests
from bs4 import BeautifulSoup


def get_trc_sender_address(tx_hash):
    url = 'https://apilist.tronscanapi.com/api/transaction-info?hash=' + tx_hash

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1)"
                             "AppleWebKit/537.36 (KHTML, like Gecko)"
                             "Chrome/86.0.4240.111 "
                             "Safari/537.36"}

    try:
        time.sleep(0.1)  # Rate limit
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.text)
            if not data:
                print("No Data Found!!")
            else:
                sender_address = data['trc20TransferInfo'][0]['from_address']
                print("TRC20 Sender address: " + sender_address)
                return sender_address
        else:
            print("Failed to Retrieve Data From: https://tronscan.org/#/transaction/" + tx_hash)
    except requests.Timeout:
        print("Request time out!!")
    except requests.RequestException as error:
        print(f'An unexpected error occured: {str(error)}')

    return 'Not Found'


# TODO: Use Web3py with Infura
def get_erc_sender_address(tx_hash):
    url = 'https://etherscan.io/tx/' + tx_hash

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1)"
                             "AppleWebKit/537.36 (KHTML, like Gecko)"
                             "Chrome/86.0.4240.111 "
                             "Safari/537.36"}
    try:
        time.sleep(0.1)
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            address_div = soup.select_one('div.col-md-9 > div > span > a[data-highlight-value]')
            if address_div:
                sender_address = address_div.text
                print("ERC20 Sender address: " + sender_address)
                return sender_address
            else:
                print("Sender's address not found.")
        else:
            print("Failed to Retrieve Data From: " + url)
    except requests.Timeout:
        print("Request time out!!")
    except requests.RequestException as error:
        print(f'An unexpected error occured: {str(error)}')

    return 'Not Found'
