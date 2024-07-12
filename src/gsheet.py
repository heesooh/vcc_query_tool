import os
import gspread
import pandas as pd
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

load_dotenv()

service_acc_path = '../credentials/service_acc_credentials.json'
workbook_id = os.getenv('GOOGLE_SHEET_ID')

csv_files = {
    'apply_records': 'apply_records.csv',
    'recharge_records': 'recharge_records.csv',
    'underpaid_records': 'underpaid_records.csv',
    'error_records': 'error_records.csv',
    'test_records': 'test_records.csv'
}


def _get_workbook():
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(service_acc_path, scope)
    client = gspread.authorize(credentials)

    workbook = client.open_by_key(workbook_id)
    return workbook


def _upload_csv_to_workbook(from_date, to_date):
    workbook = _get_workbook()

    existing_sheets = workbook.worksheets()
    sheet_names = [sheet.title for sheet in existing_sheets]

    for sheet_name, csv_file in csv_files.items():
        df = pd.read_csv(f"../data/FROM_{from_date}_TO_{to_date}/" + csv_file)
        df.fillna('', inplace=True)

        if 'order_id' in df.columns:
            df['order_id'] = df['order_id'].astype(str)

        if sheet_name in sheet_names:
            if len(existing_sheets) > 1:
                worksheet = workbook.worksheet(sheet_name)
                workbook.del_worksheet(worksheet)
                worksheet = workbook.add_worksheet(title=sheet_name, rows=len(df) + 100, cols=len(df.columns) + 10)
            else:
                worksheet = workbook.worksheet(sheet_name)
                worksheet.clear()
        else:
            worksheet = workbook.add_worksheet(title=sheet_name, rows=len(df) + 100, cols=len(df.columns) + 10)

        worksheet.update([df.columns.values.tolist()] + df.values.tolist())


def upload_to_google(from_date, to_date):
    _upload_csv_to_workbook(from_date, to_date)
