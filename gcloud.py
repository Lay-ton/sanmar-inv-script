from apiclient import discovery
from google.oauth2.service_account import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
READ_SPREADSHEET_RANGE = "Sheet1!A2:D100"
WRITE_SPREADSHEET_RANGE = "Sheet1!E2:L100"


def getDataFromSheets(spreadSheetId):
    credentials = Credentials.from_service_account_file(
        'google-credentials.json', scopes=SCOPES)
    service = discovery.build('sheets', 'v4', credentials=credentials)

    results = service.spreadsheets().values().get(
        spreadsheetId=spreadSheetId, range=READ_SPREADSHEET_RANGE).execute()

    return results['values']


def writeDataToSheets(spreadSheetId, data):
    body = {
        "values": data
    }
    credentials = Credentials.from_service_account_file(
        'google-credentials.json', scopes=SCOPES)
    service = discovery.build('sheets', 'v4', credentials=credentials)

    results = service.spreadsheets().values().update(
        spreadsheetId=spreadSheetId, range=WRITE_SPREADSHEET_RANGE, valueInputOption='RAW', body=body).execute()

    return results
