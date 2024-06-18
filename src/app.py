from data import get_records
from filter import filter_records
from revenue import calculate_card_revenue

records = get_records('2024-05-01', '2024-05-31')
filtered_records = filter_records(records)
updated_records = calculate_card_revenue(filtered_records)

print(updated_records['apply_records'].to_string())
print(updated_records['recharge_records'].to_string())
print(updated_records['underpaid_records'].to_string())
print(updated_records['error_records'].to_string())
print(updated_records['test_records'].to_string())
