import os
from dotenv import load_dotenv
from args import get_arguments
from query import get_records
from filter import filter_records
from revenue import calculate_card_revenue
from order import order_records
from gsheet import upload_to_google
from pyfiglet import Figlet
from clint.textui import puts, colored, indent
from data import is_result_exist, get_existing_data, store_order_records

load_dotenv()


def main(from_date, to_date):
    f = Figlet(font='slant')
    print(f.renderText('MW INVOICE'))

    # try:
    puts(colored.blue('Query Records: ') + f'Fetching data from {from_date} to {to_date}...')
    records = get_records(from_date, to_date)

    # records.to_csv('../data/TEST/test_result.csv', index=False)

    puts(colored.blue('Filter Records: ') +
         'Filtering records...')
    filtered_records = filter_records(records)

    # for record in filtered_records:
    #     filtered_records[record].to_csv('../data/TEST/test_filter_' + record + '.csv', index=False)

    puts(colored.blue('Calculate Revenue: ') +
         'Calculating revenue...')
    updated_records = calculate_card_revenue(filtered_records)

    # for record in updated_records:
    #     updated_records[record].to_csv('../data/TEST/test_calculation_' + record + '.csv', index=False)

    puts(colored.blue('Order Records: ') + 'Ordering filtered records before uploading to Google Sheet...')
    ordered_records = order_records(updated_records)

    # for record in ordered_records:
    #     ordered_records[record].to_csv('../data/TEST/test_order_' + record + '.csv', index=False)

    puts(colored.blue('Store Records: ') + 'Writing query result in the system database for future use...')
    store_order_records(from_date, to_date, ordered_records)

    puts(colored.blue('Upload Records: ') + 'Uploading filtered records to Google Sheet...')
    upload_to_google(from_date, to_date)

    # except Exception as e:
    #     print("project interrupted unexpectedly: ", e)


if __name__ == "__main__":
    args = get_arguments()
    if is_result_exist(args.from_date, args.to_date):
        existing_records = get_existing_data(args.from_date, args.to_date)
        puts(colored.blue('Upload Records: ') + 'Uploading existing records to Google Sheet...')
        upload_to_google(args.from_date, args.to_date)
    else:
        main(args.from_date, args.to_date)

    puts(colored.green('Complete: ') +
         "Please visit the following link to view the latest records >>> "
         f"https://docs.google.com/spreadsheets/d/{os.getenv('GOOGLE_SHEET_ID')} <<<")
