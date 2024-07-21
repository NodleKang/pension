import streamlit as st
import plotly.express as px
import altair as alt
from data.data_processor import DataProcessor
import pandas as pd
import math


def format_currency(value):
    return f"{value / 1000000:.1f}M"


def render(data_processor: DataProcessor):
    st.set_page_config(layout='wide', page_title="월별 자산")
    st.title("월별 자산")

    # 1. 데이터 가져오기
    df = data_processor.get_data("monthly_assets")

    # 2. 데이터 전처리
    df['연월'] = pd.to_datetime(df['연월'])

    # 그룹화 및 집계
    grouped_df = df.groupby(['연월', '연금여부'])['평가액'].sum().unstack(fill_value=0).reset_index()
    grouped_df['합계'] = grouped_df['연금'] + grouped_df['일반']
    grouped_df['연월_str'] = grouped_df['연월'].dt.strftime('%Y-%m')

    # 3. 테이블 생성
    st.subheader("월별 자산 평가액 테이블")
    display_df = grouped_df.copy()
    for col in ['연금', '일반', '합계']:
        display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f} 원")
    display_df = display_df[['연월_str', '연금', '일반', '합계']].rename(columns={'연월_str': '연월'})
    st.dataframe(display_df.set_index('연월').sort_index(ascending=False), use_container_width=True)

    # 4. 바 차트 생성
    st.subheader("월별 자산 평가액 바 차트")
    melted_df = grouped_df.melt(id_vars=['연월_str'], value_vars=['연금', '일반', '합계'], var_name='연금여부', value_name='평가액')

    # 평가액을 백만 원 단위로 변환
    melted_df['평가액_백만원'] = melted_df['평가액'] / 1000000

    fig = px.bar(melted_df,
                 x='연월_str',
                 y='평가액_백만원',
                 color='연금여부',
                 barmode='group',
                 labels={'연월_str': '연월', '평가액_백만원': '평가액 (백만원)', '연금여부': '연금여부'},
                 title='연월별 평가액')

    fig.update_layout(
        xaxis_title='연월',
        yaxis_title='평가액 (백만원)',
        legend_title='연금여부',
        font=dict(size=12),
        height=500,
        width=800
    )

    # x축 설정
    fig.update_xaxes(
        tickmode='array',
        tickvals=melted_df['연월_str'].unique(),
        ticktext=melted_df['연월_str'].unique(),
        tickangle=45
    )

    # y축 포맷 설정
    fig.update_yaxes(tickformat=",d", title_text="평가액 (백만원)")

    # 막대 위에 값 표시
    fig.update_traces(texttemplate='%{y:.1f} 백만원', textposition='outside')

    st.plotly_chart(fig, use_container_width=True)


# Streamlit 멀티페이지 앱 기능 활용
if __name__ == "__main__":
    if 'data_processor' in st.session_state:
        render(st.session_state['data_processor'])
    else:
        st.error("Please run the main app first to initialize data.")