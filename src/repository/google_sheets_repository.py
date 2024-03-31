from typing import List, Optional
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound
import pandas as pd
import decimal

#
from .data_repository import DataRepository

class GoogleSheetsRepository(DataRepository):
    def __init__(self, credentials_file: Optional[str] = None):
        self.credentials_file = credentials_file or 'resources/credentials/credential.json'
        try:
            self.client = self.authenticate()
        except Exception as e:
            print(f"인증 중 오류 발생: {e}")
            self.client = None

    def authenticate(self) -> gspread.Client:
        try:
            credentials_path = self.credentials_file
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
            )
            return gspread.authorize(credentials)
        except Exception as e:
            print(f"자격 증명 로드 중 오류 발생: {e}")
            raise

    def list_spreadsheets(self) -> List[dict]:
        try:
            return [spreadsheet['name'] for spreadsheet in self.client.list_spreadsheet_files()]
        except Exception as e:
            print(f"스프레드시트 목록 조회 중 오류 발생: {e}")
            return []

    def get_sheet(self, spreadsheet_id: str) -> gspread.Spreadsheet:
        try:
            return self.client.open_by_key(spreadsheet_id)
        except SpreadsheetNotFound as e:
            print(f"스프레드시트 찾기 오류: {e}")
            return None
        except Exception as e:
            print(f"스프레드시트 열기 중 오류 발생: {e}")
            return None

    def get_worksheet_names(self, spreadsheet_name: str) -> List[str]:
        try:
            spreadsheet = self.client.open(spreadsheet_name)
            return [worksheet.title for worksheet in spreadsheet.worksheets()]
        except SpreadsheetNotFound as e:
            print(f"스프레드시트 찾기 오류: {e}")
            return []
        except Exception as e:
            print(f"워크시트 목록 조회 중 오류 발생: {e}")
            return []

    def get_range_data(self, spreadsheet_name: str, worksheet_name: str, cell_range: str) -> pd.DataFrame:
        try:
            spreadsheet = self.client.open(spreadsheet_name)
            worksheet = spreadsheet.worksheet(worksheet_name)
            # gspread의 get_all_values 메소드를 사용하여 셀 범위의 데이터를 리스트의 리스트 형태로 가져옵니다.
            data = worksheet.get(cell_range)

            # 데이터가 비어있는 경우 빈 DataFrame 반환
            if not data or len(data) < 2:
                return pd.DataFrame()

            # 첫 번째 행을 컬럼명으로 사용하여 DataFrame을 생성합니다.
            df = pd.DataFrame(data[1:], columns=data[0])
            return df
        except (SpreadsheetNotFound, WorksheetNotFound) as e:
            print(f"스프레드시트 또는 워크시트 찾기 오류: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"셀 범위 조회 중 오류 발생: {e}")
            return pd.DataFrame()

    def get_all_data(self, spreadsheet_name: str, worksheet_name: str) -> pd.DataFrame:
        try:
            spreadsheet = self.client.open(spreadsheet_name)
            worksheet = spreadsheet.worksheet(worksheet_name)
            # 워크시트의 모든 데이터를 가져옵니다.
            data = worksheet.get_all_values()

            # 데이터가 비어있는 경우 빈 DataFrame 반환
            if not data or len(data) < 2:
                return pd.DataFrame()

            # 첫 번째 행을 컬럼명으로 사용
            df = pd.DataFrame(data[1:], columns=data[0])

            # '입금', '출금', '자산', '금액'으로 끝나는 필드명을 가진 컬럼의 데이터는 decimal로 변환
            for column in df.columns:
                if column.endswith(('입금', '출금', '자산', '금액', '가액')):
                    df[column] = df[column].apply(
                        lambda x: decimal.Decimal(x.replace(',', '')) if x else decimal.Decimal(0))

            return df
        except (SpreadsheetNotFound, WorksheetNotFound) as e:
            print(f"스프레드시트 또는 워크시트 찾기 오류: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return pd.DataFrame()
