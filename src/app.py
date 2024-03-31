from model.portfolio import ModelPortfolio
from repository.google_sheets_repository import GoogleSheetsRepository
import pandas as pd
import yaml
import streamlit as st

# YAML 설정 파일을 로드하는 함수
def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# 데이터 리포지토리 객체를 생성하는 함수
def get_data_repository(config):
    data_source_type = config['data_source']['type']
    if data_source_type == 'google_sheets':
        return GoogleSheetsRepository(config['google_sheets']['credentials_path'])
    else:
        raise ValueError("Unsupported data source type")

def get_recent_month(data) -> str:
    return data['연월'].max()

def display_recent_month_end_data(data):
    recent_month = get_recent_month(data)
    recent_month_end_data = data[data['연월'] == recent_month]

    st.header(recent_month+" 계좌별 자산 현황")
    st.dataframe(recent_month_end_data)

def main():

    config = load_config('D:/Workspace/pension/resources/config/config.yaml')

    repository = get_data_repository(config)

    db_name = config['data_source']['spreadsheet_name']

    # 계좌 데이터를 가져옵니다
    table_name = config['tables']['accounts']
    accounts = repository.get_all_data(db_name, table_name)

    # (이력포함)월말자산 데이터를 가져옵니다
    table_name = config['tables']['month_end_assets']
    month_end_assets = repository.get_all_data(db_name, table_name)

    # 계좌 데이터와 (이력포함) 월말자산 데이터를 조인합니다.
    month_end_assets = pd.merge(accounts, month_end_assets, on="계좌아이디")

    # 가장 최근 월말
    display_recent_month_end_data(month_end_assets)

    mp = ModelPortfolio('퇴직연금', '성장형')

    mp = ModelPortfolio('퇴직연금', '중립형')

    mp = ModelPortfolio('퇴직연금', '안정형')

    mp = ModelPortfolio('연금저축', '성장형')

    mp = ModelPortfolio('연금저축', '중립형')

    mp = ModelPortfolio('연금저축', '안정형')


if __name__ == "__main__":
    main()