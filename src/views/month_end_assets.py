import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff


MONTH_END_ASSETS = "month_end_assets"


def view_month_end_assets(all_df: dict):
    df : pd.DataFrame = all_df[MONTH_END_ASSETS]

    st.header("월말 자산")

    ####
    summary_col = st.columns(1)
    with summary_col[0]:
        total_value = df['평가액'].sum()
        print(total_value)
        formatted_total_value = f"{total_value:,}원"
        st.write(f'현재 자산 총액은 {formatted_total_value} 입니다.')

    ####
    yyyymm_col, column_col = st.columns(2)
    with yyyymm_col:
        yyyymm_list = [i for i in df['연월'].unique()]
        selected_yyyymms = st.multiselect("연월을 선택하세요:", yyyymm_list)
    with column_col:
        column_list = df.columns.tolist()
        selected_columns = st.multiselect("그룹핑 컬럼을 선택하세요:", column_list)

    ####
    table_col, chart_col = st.columns(2)
    with table_col:
        st.container()  # 첫 번째 하단 컨테이너
        st.dataframe(df)

    with chart_col:
        st.container()  # 첫 번째 하단 컨테이너
        # pie 차트 작성
        fig = px.pie(df, names='연금여부', values='평가액', title='평가액 비중')
        st.plotly_chart(fig)
