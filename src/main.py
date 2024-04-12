from models.portfolio import ModelPortfolio
from services.config import Config
from repositories.data_repository import DataRepository
from repositories.google_sheets_repository import GoogleSheetsRepository
import pandas as pd
import yaml
import streamlit as st
from streamlit_option_menu import option_menu
from views.month_end_assets import view_month_end_assets
from views.accounts import view_accounts


# YAML 설정 파일을 로드하는 함수
def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


# 데이터 리포지토리 객체를 생성하는 함수
def create_data_repository(config) -> DataRepository:
    data_source_type = config['data_source']['type']
    if data_source_type == 'google_sheets':
        return GoogleSheetsRepository(config['google_sheets']['credentials_path'])
    else:
        raise ValueError("Unsupported data source type")


# 화면 출력
def view(config: Config, repository: DataRepository):
    st.set_page_config(layout='wide')

    with st.sidebar:
        menu_selection = option_menu("자산관리",
                             options=["계좌현황", "월말자산", "연금관리"],
                             menu_icon="list",)

    if menu_selection == "계좌현황":
        view_accounts(config, repository)
    elif menu_selection == "월말자산":
        view_month_end_assets(config, repository)

def main():

    #### 초기화 ####
    config = load_config('C:/Workspace/pension/resources/config/config.yaml')
    repository = create_data_repository(config)

    #### View ####
    view(config, repository)


if __name__ == "__main__":
    main()
