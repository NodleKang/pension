import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff


MONTH_END_ASSETS = "month_end_assets"


def view_month_end_assets(all_df: dict):
    df : pd.DataFrame = all_df[MONTH_END_ASSETS]

    st.header("월말 자산")

    # 첫번째 행
    col1 = st.columns(1)
    with col1[0]:
        total_value = df['평가액'].sum()
        print(total_value)
        formatted_total_value = f"{total_value:,}원"
        st.write(f'현재 자산 총액은 {formatted_total_value} 입니다.')

    # 두번째 행
    col2 = st.columns(2)
    with col2[0]:
        yyyymm_list = [i for i in df['연월'].unique()]
        selected_yyyymms = st.multiselect("연월을 선택하세요:", yyyymm_list)
    with col2[1]:
        column_list = df.columns.tolist()
        selected_columns = st.multiselect("그룹핑 컬럼을 선택하세요:", column_list)

    # 세번째 행
    col3 = st.columns(1)
    with col3[0]:
        st.container()  # 첫 번째 하단 컨테이너
        # pie 차트 작성
        fig = px.treemap(df, path=['연금여부', '계좌특징'], values='평가액', title='비중 분포')
        st.plotly_chart(fig)


    # 네번째 행
    col4 = st.columns(1)
    with col4[0]:
        st.container()  # 첫 번째 하단 컨테이너
        st.dataframe(df)
