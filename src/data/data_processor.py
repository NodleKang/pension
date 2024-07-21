from typing import Dict

import pandas as pd

from data.data_loader import DataLoader
from data.cache_manager import CacheManager


class DataProcessor:
    def __init__(self, data_loader: DataLoader, cache_manager: CacheManager):
        self.data_loader = data_loader
        self.cache_manager = cache_manager
        self.data: Dict[str, pd.DataFrame] = {}

    def load_and_cache_data(self):
        self.data = self.data_loader.load_data()
        for key, df in self.data.items():
            self.cache_manager.cache_data(key, df)

    def get_data(self, key: str) -> pd.DataFrame:
        return self.cache_manager.get_cached_data(key)

###########################################################
    def load_and_process_data(self):

        @self.cache_manager.cache
        def _load_and_process():

            data_dict = self.data_loader.load_data()
            accounts = data_dict["accounts"]
            monthly_assets = data_dict["monthly_assets"]
            pension_portfolio = data_dict["pension_portfolio"]

            # 데이터 타입 최적화
            self.optimize_dtypes(accounts)
            self.optimize_dtypes(monthly_assets)
            self.optimize_dtypes(pension_portfolio)

            return {"accounts": accounts, "monthly_assets": monthly_assets, "pension_portfolio": pension_portfolio}

        return _load_and_process

    def optimize_dtypes(self, df: pd.DataFrame):
        # 데이터 타입 최적화
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = pd.to_datetime(df[col], errors='ignore')
                if df[col].dtype == 'object':
                    df[col] = df[col].astype('category')
            elif df[col].dtype == 'float64':
                df[col] = df[col].astype('float32')
            elif df[col].dtype == 'int64':
                df[col] = df[col].astype('int32')

    def get_unique_yyyymm(self) -> pd.Series:
        return self.processed_data["month_end_assets"]["yyyymm"].unique()

    def filter_data_by_yyyymm(self, yyyymm: str) -> pd.DataFrame:
        return self.processed_data["monthly_assets"][self.processed_data["monthly_assets"]["yyyymm"] == yyyymm]

    def get_data_count_by_yyyymm(self) -> pd.DataFrame:
        return self.processed_data["month_end_assets"]["yyyymm"].value_counts().reset_index()
