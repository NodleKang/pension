from typing import List, Dict
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


class GoogleSheetsHelper:
    def __init__(self, credentials_path: str):
        self.credentials_name = credentials_path
        self.client = self._authenticate()

    def _authenticate(self) -> gspread.Client:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_name, scope)
        return gspread.authorize(credentials)

    def get_spreadsheet_id(self, spreadsheet_name: str) -> str:
        all_spreadsheets = self.client.list_spreadsheet_files()
        for sheet in all_spreadsheets:
            if sheet['name'] == spreadsheet_name:
                return sheet['id']
        return None

    def get_worksheet_as_dataframe(self, spreadsheet_id: str, worksheet_name: str) -> pd.DataFrame:
        worksheet = self.client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        data = worksheet.get_all_values()
        return pd.DataFrame(data[1:], columns=data[0])
