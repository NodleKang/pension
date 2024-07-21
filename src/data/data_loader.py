from typing import Dict
from utils.google_sheets_helper import GoogleSheetsHelper
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import decimal


class DataLoader:
    """
    Google Sheets에서 데이터를 로드하고 처리하는 클래스입니다.

    이 클래스는 Google Sheets API를 사용하여 특정 스프레드시트에서 데이터를 로드하고,
    로드된 데이터를 pandas DataFrame으로 변환한 후 필요한 전처리를 수행합니다.

    Attributes:
        google_sheets_helper (GoogleSheetsHelper): Google Sheets API 사용을 위한 헬퍼 객체
        spreadsheet_id (str): 데이터를 로드할 Google 스프레드시트의 ID
        worksheets_config (Dict[str, str]): 각 워크시트의 이름을 매핑한 설정 딕셔너리
    """
    def __init__(self,
                 google_sheets_config: Dict[str, str],
                 worksheets_config: Dict[str, str]):
        """
        DataLoader 클래스의 인스턴스를 초기화합니다.

        Args:
            google_sheets_config (Dict[str, str]): Google Sheets 연결 설정
            worksheets_config (Dict[str, str]): 워크시트 이름 매핑 설정
        """
        self.google_sheets_helper = GoogleSheetsHelper(google_sheets_config["credentials_path"])
        self.spreadsheet_id = self.google_sheets_helper.get_spreadsheet_id(google_sheets_config["spreadsheet_name"])
        self.worksheets_config = worksheets_config

    def load_data(self) -> Dict[str, pd.DataFrame]:
        """
        설정된 Google 스프레드시트에서 데이터를 로드하고 처리합니다.

        Returns:
            Dict[str, pd.DataFrame]: 처리된 데이터프레임들을 담은 딕셔너리
        """
        # 계좌
        accounts_df = (self.google_sheets_helper
                       .get_worksheet_as_dataframe(self.spreadsheet_id,
                                                   self.worksheets_config["accounts"]))
        # 월말자산
        monthly_assets_df = (self.google_sheets_helper
                               .get_worksheet_as_dataframe(self.spreadsheet_id,
                                                           self.worksheets_config["monthly_assets"]))
        monthly_assets_df = pd.merge(monthly_assets_df, accounts_df, on='계좌아이디', how='left')
        monthly_assets_df['연금여부'] = monthly_assets_df['연금여부'].apply(lambda x: "연금" if x == 'Y' else "일반")

        # 입출금
        io_history_df = (self.google_sheets_helper
                                .get_worksheet_as_dataframe(self.spreadsheet_id,
                                                            self.worksheets_config["io_history"]))
        return {
            "accounts": self._df_manufacture(accounts_df),
            "monthly_assets": self._df_manufacture(monthly_assets_df),
            "io_history": self._df_manufacture(io_history_df)
        }

    def _df_manufacture(self, df: pd.DataFrame):
        """
        데이터프레임의 특정 컬럼들을 전처리합니다.

        - 금액 관련 컬럼을 decimal 타입으로 변환
        - '연월' 컬럼을 date 타입으로 변환하고 각 달의 마지막 날로 설정

        Args:
            df (pd.DataFrame): 전처리할 데이터프레임

        Returns:
            pd.DataFrame: 전처리된 데이터프레임
        """
        for column in df.columns:
            # '입금', '출금', '자산', '금액'으로 끝나는 필드명을 가진 컬럼의 데이터는 decimal로 변환
            if column.endswith(('입금', '출금', '자산', '금액', '가액')):
                df[column] = df[column].apply(
                    lambda x: decimal.Decimal(x.replace(',', '')) if x else decimal.Decimal(0))
            # 연월 필드의 데이터 타입을 date 타입으로 변환하고, 각 달의 마지막 날로 설정
            if column == '연월':
                df['연월'] = pd.to_datetime(df['연월']) + MonthEnd(1)
        return df
