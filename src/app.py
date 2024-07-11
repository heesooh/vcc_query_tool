import os
from dotenv import load_dotenv
from args import get_arguments
from data import get_records
from filter import filter_records
from revenue import calculate_card_revenue
from order import order_records
from gsheet import upload_to_google
from pyfiglet import Figlet
from clint.textui import puts, colored, indent

load_dotenv()


def main(from_date, to_date):
    f = Figlet(font='slant')
    print(f.renderText('VCC INVOICE'))

    with indent(4, quote='>>>'):
        puts(colored.blue('Query Records: ') + f'Fetching data from {from_date} to {to_date}...')
        records = get_records(from_date, to_date)

        puts(colored.blue('Filter Records: ') +
             'Filtering records into \'apply\', \'recharge\', \'underpaid\', \'error\', and \'test\' tables...')
        filtered_records = filter_records(records)

        puts(colored.blue('Calculate Revenue: ') +
             'Calculating \'transaction fee\', \'commission\', and \'irregular payment amount\'...')
        updated_records = calculate_card_revenue(filtered_records)

        puts(colored.blue('Order Records: ') + 'Ordering filtered records before uploading to Google Sheet...')
        ordered_records = order_records(updated_records)

        puts(colored.blue('Upload Records: ') + 'Uploading filtered records to Google Sheet...')
        upload_to_google(ordered_records)

        puts(colored.blue('Complete: ') + "Please visit the following link to view the latest records >>> "
        f"https://docs.google.com/spreadsheets/d/{os.getenv('GOOGLE_SHEET_ID')} <<<")


if __name__ == "__main__":
    args = get_arguments()
    main(args.from_date, args.to_date)
