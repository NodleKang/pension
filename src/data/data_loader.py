from typing import Dict
from utils.google_sheets_helper import GoogleSheetsHelper
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import decimal


class DataLoader:
    def __init__(self,
                 google_sheets_config: Dict[str, str],
                 worksheets_config: Dict[str, str]):
        self.google_sheets_helper = GoogleSheetsHelper(google_sheets_config["credentials_path"])
        self.spreadsheet_id = self.google_sheets_helper.get_spreadsheet_id(google_sheets_config["spreadsheet_name"])
        self.worksheets_config = worksheets_config

    def load_data(self) -> Dict[str, pd.DataFrame]:
        accounts_df = (self.google_sheets_helper
                       .get_worksheet_as_dataframe(self.spreadsheet_id,
                                                   self.worksheets_config["accounts"]))
        month_end_assets_df = (self.google_sheets_helper
                               .get_worksheet_as_dataframe(self.spreadsheet_id,
                                                           self.worksheets_config["month_end_assets"]))
        pension_portfolio_df = (self.google_sheets_helper
                                .get_worksheet_as_dataframe(self.spreadsheet_id,
                                                            self.worksheets_config["pension_portfolio"]))
        return {
            "accounts": self._df_manufacture(accounts_df),
            "month_end_assets": self._df_manufacture(month_end_assets_df),
            "pension_portfolio": self._df_manufacture(pension_portfolio_df)
        }

    def _df_manufacture(self, df: pd.DataFrame):
        for column in df.columns:
            # '입금', '출금', '자산', '금액'으로 끝나는 필드명을 가진 컬럼의 데이터는 decimal로 변환
            if column.endswith(('입금', '출금', '자산', '금액', '가액')):
                df[column] = df[column].apply(
                    lambda x: decimal.Decimal(x.replace(',', '')) if x else decimal.Decimal(0))
            # 연월 필드의 데이터 타입을 date 타입으로 변환하고, 각 달의 마지막 날로 설정
            if column == '연월':
                df['연월'] = pd.to_datetime(df['연월']) + MonthEnd(1)
        return df
