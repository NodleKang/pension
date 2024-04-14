from typing import Optional
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import decimal

#
from .data_source import DataSource
import streamlit as st


class GoogleSheetsSource(DataSource):
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

    def load_data(self, spreadsheet_name: str, worksheet_name: str) -> pd.DataFrame:
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

            # 컬럼 가공
            for column in df.columns:
                # '입금', '출금', '자산', '금액'으로 끝나는 필드명을 가진 컬럼의 데이터는 decimal로 변환
                if column.endswith(('입금', '출금', '자산', '금액', '가액')):
                    df[column] = df[column].apply(
                        lambda x: decimal.Decimal(x.replace(',', '')) if x else decimal.Decimal(0))
                # 연월 필드의 데이터 타입을 date 타입으로 변환하고, 각 달의 마지막 날로 설정
                if column == '연월':
                    df['연월'] = pd.to_datetime(df['연월']) + MonthEnd(1)

            return df
        except (SpreadsheetNotFound, WorksheetNotFound) as e:
            print(f"스프레드시트 또는 워크시트 찾기 오류: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return pd.DataFrame()
