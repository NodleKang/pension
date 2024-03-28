import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def authenticate():
    """OAuth 2.0 클라이언트 ID를 사용하여 Google Sheets API에 인증하는 함수"""
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client


def get_sheet_names(spreadsheet_id):
    """Google Sheets에서 시트 목록을 가져오는 함수"""
    client = authenticate()
    sheet = client.open_by_key(spreadsheet_id)
    sheet_list = sheet.worksheets()
    sheet_names = [ws.title for ws in sheet_list]
    return sheet_names


def get_all_cells(sheet_id, range_name):
    """특정 시트의 모든 셀 내용을 가져오는 함수"""
    client = authenticate()
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(range_name)
    data = worksheet.get_all_values()
    if not data:
        print('No data found.')
    else:
        df = pd.DataFrame(data[1:], columns=data[0])
        return df


# 예시 코드
if __name__ == "__main__":
    # 구글 시트 ID
    spreadsheet_id = 'your_spreadsheet_id'
    # 가져올 시트의 이름
    sheet_name = 'Sheet1'
    # 가져올 시트 내용의 범위 (예: A1:B10)
    range_name = 'A1:B2'

    print("시트 목록:", get_sheet_names(spreadsheet_id))
    print("셀 내용:", get_all_cells(spreadsheet_id, range_name))
