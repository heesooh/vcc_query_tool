import os
import pandas as pd
from datetime import datetime
from clint.textui import puts, colored, indent


def _get_directory_path(from_date, to_date):
    return f"../data/FROM_{from_date}_TO_{to_date}"


def _is_duplicate(directory):
    if os.path.exists(directory):
        return True
    return False


def get_existing_data(from_date, to_date):
    directory = _get_directory_path(from_date, to_date)
    dfs = {}

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            dfs[filename[:-4]] = pd.read_csv(file_path)

    return dfs


def _get_create_time(directory):
    file_path = directory + "/create_time.txt"

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
        return None
    except IOError:
        print("Error while reading the file.")
        return None


def is_exist(from_date, to_date):
    directory = _get_directory_path(from_date, to_date)
    if _is_duplicate(directory):
        create_time = _get_create_time(directory)

        puts(colored.red('System Alert: '))

        with indent(4, quote='>>>'):
            puts("Requested data from " +
                 colored.red(f"{from_date} to {to_date} ") +
                 "already exists."
                 "\nThis query result was created: " +
                 colored.red(f"{create_time}"))

        puts(colored.green("Would you like to upload the existing data instead?"))
        with indent(4, quote='>>>'):

            user_response = input(">>> (yes/no): ")
            if user_response.lower() in ['yes', 'ye', 'y']:
                return True

    return False


def store_data(from_date, to_date, records):
    directory = _get_directory_path(from_date, to_date)

    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        with indent(4, quote='>>>'):
            puts(colored.red("Overwriting existing data"))

    for key, df in records.items():
        csv_path = os.path.join(directory, f"{key}.csv")
        df.to_csv(csv_path, index=False)
        with indent(4, quote='>>>'):
            puts(colored.yellow(f"Saved: {csv_path}"))

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_txt_path = os.path.join(directory, "create_time.txt")
    with open(time_txt_path, 'w') as file:
        file.write(current_time)
        with indent(4, quote='>>>'):
            puts(colored.yellow(f"Saved: {time_txt_path}"))
