import os
from dotenv import load_dotenv
import argparse
from database import get_records
from filter import filter_records
from revenue import calculate_card_revenue
from order import order_records
from gsheet import upload_to_google
from pyfiglet import Figlet
from clint.textui import puts, colored, indent
from data import is_exist, get_existing_data, store_data

load_dotenv('../credentials/.env')


def _get_arguments():
    parser = argparse.ArgumentParser(description='Process records between two dates.')
    parser.add_argument('-f', '--from-date', required=True, type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('-t', '--to-date', required=True, type=str, help='End date in YYYY-MM-DD format')

    return parser.parse_args()


def main(from_date, to_date):
    f = Figlet(font='slant')
    print(f.renderText('MW INVOICE'))

    puts(colored.blue('Query Records: ') + f'Fetching data from {from_date} to {to_date}...')
    records = get_records(from_date, to_date)

    puts(colored.blue('Filter Records: ') + 'Filtering records...')
    filtered_records = filter_records(records)

    puts(colored.blue('Calculate Revenue: ') + 'Calculating revenue...')
    updated_records = calculate_card_revenue(filtered_records)

    puts(colored.blue('Order Records: ') + 'Ordering filtered records before uploading to Google Sheet...')
    ordered_records = order_records(updated_records)

    puts(colored.blue('Store Records: ') + 'Writing query result in the system database for future use...')
    store_data(from_date, to_date, ordered_records)

    puts(colored.blue('Upload Records: ') + 'Uploading filtered records to Google Sheet...')
    upload_to_google(from_date, to_date)


if __name__ == "__main__":
    main('2024-11-01', '2024-11-30')

    # args = _get_arguments()
    #
    # try:
    #     if is_exist(args.from_date, args.to_date):
    #         existing_records = get_existing_data(args.from_date, args.to_date)
    #         puts(colored.blue('Upload Records: ') + 'Uploading existing records to Google Sheet...')
    #         upload_to_google(args.from_date, args.to_date)
    #     else:
    #         # main(args.from_date, args.to_date)
    #         main('2024-11-01', '2024-11-30')
    # except Exception as e:
    #     print('Unexpected error has occurred: ', e)

    puts(colored.green('Complete: ') +
         "Please visit the following link to view the latest records >>> "
         f"https://docs.google.com/spreadsheets/d/{os.getenv('GOOGLE_SHEET_ID')} <<<")
