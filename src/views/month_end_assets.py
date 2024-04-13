import streamlit as st
import plotly.express as px


MONTH_END_ASSETS = "month_end_assets"


def view_month_end_assets(all_df: dict):
    df = all_df[MONTH_END_ASSETS]

    st.header("월말 자산")

    yyyymmCol, columnCol = st.columns(2)
    with yyyymmCol:
        yyyymm_list = [i for i in df['연월'].unique()]
        selected_yyyymms = st.multiselect("연월을 선택하세요:", yyyymm_list)
    with columnCol:
        column_list = df.columns.tolist()
        selected_columns = st.multiselect("그룹핑 컬럼을 선택하세요:", column_list)

    tableCol, chartCol = st.columns(2)

    with tableCol:
        st.container()  # 첫 번째 하단 컨테이너
        st.dataframe(df)

    with chartCol:
        st.container()  # 첫 번째 하단 컨테이너
        # pie 차트 작성
        pie_data = px.pie(df, names='상품성격', values='평가액', title='상품성격별 평가액 비중')
        st.plotly_chart(pie_data)
