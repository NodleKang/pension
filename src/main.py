from models.portfolio import ModelPortfolio
from services.config import Config
from repositories.data_source_factory import DataSourceFactory
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from views.month_end_assets import view_month_end_assets
from views.accounts import view_accounts


# 화면 출력
def view(all_df: dict):
    st.set_page_config(layout='wide')

    with st.sidebar:
        menu_selection = option_menu("자산관리",
                             options=["월말자산", "연금관리", "계좌현황"],
                             menu_icon="list",)

    if menu_selection == "계좌현황":
        view_accounts(all_df)
    elif menu_selection == "월말자산":
        view_month_end_assets(all_df)

def main():

    #### 초기화 ####
    config = Config('C:/Workspace/pension/resources/config/config.yaml')
    data_source = DataSourceFactory.get_data_source(config)

    #### 데이터 로드 ####
    all_df = {}
    db_name, table_name = config.get_source_identifiers("accounts")
    df = data_source.load_data(db_name, table_name)
    all_df["accounts"] = df

    db_name, table_name = config.get_source_identifiers("month_end_assets")
    df = data_source.load_data(db_name, table_name)
    all_df["month_end_assets"] = pd.merge(all_df["accounts"], df, on="계좌아이디")

    #### View ####
    view(all_df)

if __name__ == "__main__":
    main()
