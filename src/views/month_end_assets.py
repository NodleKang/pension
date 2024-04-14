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
        formatted_total_value = f"{total_value:,}원"
        st.write(f'현재 자산 총액은 {formatted_total_value} 입니다.')

    # 두번째 행
    col2 = st.columns(1)
    with col2[0]:
        # 연월 선택을 위한 슬라이더
        yyyymm_list = [i for i in df['연월'].unique()]
        yyyymm_slider = st.slider(
            "연월을 선택하세요:",
            min_value=yyyymm_list[0].to_pydatetime(),
            max_value=yyyymm_list[-1].to_pydatetime(),
            value=yyyymm_list[0].to_pydatetime(),
            format='YYYY-MM'
        )
        # 슬라이더에 선택된 연월에 해당하는 데이터 필터링
        filtered_data = df[df['연월'] == yyyymm_slider]

    # 세번째 행
    col3 = st.columns(1)
    with col3[0]:
        st.container()  # 첫 번째 하단 컨테이너
        fig = px.treemap(
            filtered_data,
            path=['해지가능', '계좌특징'],
            values='평가액',
        )
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0)  # 상단, 하단, 좌측, 우측 마진 크기를 조정합니다.
        )
        st.plotly_chart(fig, use_container_width=True)

    # 네번째 행
    col4 = st.columns(1)
    with col4[0]:
        st.container()  # 첫 번째 하단 컨테이너
        st.dataframe(filtered_data)
