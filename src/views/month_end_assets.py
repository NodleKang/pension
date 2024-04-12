import plotly.express
import streamlit as st
import pandas as pd
import plotly.express as px
from services.config import Config
from repositories.data_repository import DataRepository


def view_month_end_assets(config: Config, repository: DataRepository):
    db_name = config['data_source']['spreadsheet_name']

    # 계좌 데이터를 가져옵니다
    table_name = config['tables']['accounts']
    accounts = repository.get_all_data(db_name, table_name)

    # (이력포함)월말자산 데이터를 가져옵니다
    table_name = config['tables']['month_end_assets']
    month_end_assets = repository.get_all_data(db_name, table_name)

    # 계좌 데이터와 (이력포함) 월말자산 데이터를 조인합니다.
    month_end_assets = pd.merge(accounts, month_end_assets, on="계좌아이디")

    # Header
    st.header("월말 자산")

    #
    yyyymmCol, columnCol = st.columns(2)
    with yyyymmCol:
        yyyymm_list = [i for i in month_end_assets['연월'].unique()]
        selected_yyyymms = st.multiselect("연월을 선택하세요:", yyyymm_list)
    with columnCol:
        column_list = month_end_assets.columns.tolist()
        selected_columns = st.multiselect("그룹핑 컬럼을 선택하세요:", column_list)

    tableCol, chartCol = st.columns(2)

    with tableCol:
        st.container()  # 첫 번째 하단 컨테이너
        st.dataframe(month_end_assets)

    with chartCol:
        st.container()  # 첫 번째 하단 컨테이너
        # pie 차트 작성
        pie_data = px.pie(month_end_assets, names='상품성격', values='평가액', title='상품성격별 평가액 비중')
        st.plotly_chart(pie_data)
