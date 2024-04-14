from unittest import TestCase

import pandas as pd
import services
from repositories.data_source_factory import DataSourceFactory
import streamlit as st

TABLES = ["accounts", "month_end_assets"]

class Test(TestCase):

    def test_load_config(self):
        #### 초기화 ####
        config = services.Config('C:/Workspace/pension/resources/config/config.yaml')
        data_source = DataSourceFactory.get_data_source(config)

        #### 데이터 로드 ####
        all_df = {}
        db_name, table_name = config.get_source_identifiers("accounts")
        df = data_source.load_data(db_name, table_name)
        all_df["accounts"] = df

        db_name, table_name = config.get_source_identifiers("month_end_assets")
        df = data_source.load_data(db_name, table_name)
        all_df["month_end_assets"] = pd.merge(all_df["accounts"], df, on="계좌아이디")

        yyyymm_list = [i for i in df['연월'].unique()]

        print(all_df)