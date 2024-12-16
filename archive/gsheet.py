import os.path
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv('../credentials/.env')

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SAMPLE_RANGE_NAME = "Sheet1!A1"


def gsheet_write():
    """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("../credentials/gsheet_token.json"):
        creds = Credentials.from_authorized_user_file("../credentials/gsheet_token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "../credentials/gsheet_credential.json", SCOPES
            )
            creds = flow.run_local_server(port=3000)
        # Save the credentials for the next run
        with open("../credentials/gsheet_token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API

        valueData = [['new', 'data'], ['data']]

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=SAMPLE_RANGE_NAME,
                valueInputOption="USER_ENTERED",
                body={"values": valueData}
            )
            .execute()
        )
        # values = result.get("values", [])
        #
        # if not values:
        #     print("No data found.")
        #     return
        #
        # print("Name, Major:")
        # for row in values:
        #     # Print columns A and E, which correspond to indices 0 and 4.
        #     print(f"{row[0]}, {row[4]}")
    except HttpError as err:
        print(err)
