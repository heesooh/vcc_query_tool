from data import get_records
from filter import filter_records
from revenue import calculate_card_revenue
from gsheet import upload_to_google

if __name__ == '__main__':
    records = get_records('2024-05-28', '2024-05-31')
    filtered_records = filter_records(records)
    updated_records = calculate_card_revenue(filtered_records)
    upload_to_google(updated_records)
