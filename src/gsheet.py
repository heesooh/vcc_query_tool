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
    'apply_records': '../data/apply_records.csv',
    'recharge_records': '../data/recharge_records.csv',
    'underpaid_records': '../data/underpaid_records.csv',
    'error_records': '../data/error_records.csv',
    'test_records': '../data/test_records.csv'
}


def _get_workbook():
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(service_acc_path, scope)
    client = gspread.authorize(credentials)

    workbook = client.open_by_key(workbook_id)
    return workbook


def _upload_csv_to_workbook():
    workbook = _get_workbook()

    existing_sheets = workbook.worksheets()
    sheet_names = [sheet.title for sheet in existing_sheets]

    for sheet_name, csv_file in csv_files.items():
        df = pd.read_csv(csv_file)
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


def _write_csv(records):
    records['apply_records'].astype(str).to_csv("../data/apply_records.csv", index=False)
    records['recharge_records'].astype(str).to_csv("../data/recharge_records.csv", index=False)
    records['underpaid_records'].astype(str).to_csv("../data/underpaid_records.csv", index=False)
    records['error_records'].astype(str).to_csv("../data/error_records.csv", index=False)
    records['test_records'].astype(str).to_csv("../data/test_records.csv", index=False)


def upload_to_google(records):
    _write_csv(records)
    _upload_csv_to_workbook()
