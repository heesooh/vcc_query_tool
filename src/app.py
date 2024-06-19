from args import get_arguments
from data import get_records
from filter import filter_records
from revenue import calculate_card_revenue
from gsheet import upload_to_google

if __name__ == '__main__':
    args = get_arguments()
    records = get_records(args.from_date, args.to_date)
    filtered_records = filter_records(records)
    updated_records = calculate_card_revenue(filtered_records)
    upload_to_google(updated_records)
