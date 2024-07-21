import streamlit as st
import plotly.express as px
from data.data_processor import DataProcessor
import pandas as pd
import math

def format_currency(value):
    return f"{value / 1000:.0f}K"

def render(data_processor: DataProcessor):
    st.set_page_config(layout='wide', page_title="월별 자산")
    st.title("월별 자산")

    # 1. 데이터 가져오기
    monthly_assets_df = data_processor.get_data("monthly_assets")
    accounts_df = data_processor.get_data("accounts")

    # 2. 데이터 전처리
    monthly_assets_df['연월'] = pd.to_datetime(monthly_assets_df['연월'])

    # 연금여부 처리
    accounts_df['연금여부'] = accounts_df['연금여부'].apply(lambda x: '연금' if x == 'Y' else '비연금')

    # 데이터 조인
    merged_df = pd.merge(monthly_assets_df, accounts_df[['계좌아이디', '연금여부']], on='계좌아이디', how='left')

    # 연금여부가 NaN인 경우 '비연금'으로 처리
    merged_df['연금여부'] = merged_df['연금여부'].fillna('비연금')

    # 그룹화 및 집계
    grouped_df = merged_df.groupby(['연월', '연금여부'])['평가액'].sum().unstack(fill_value=0).reset_index()
    grouped_df['합계'] = grouped_df['연금'] + grouped_df['비연금']
    grouped_df['연월_str'] = grouped_df['연월'].dt.strftime('%Y-%m')

    # 3. 테이블 생성
    st.subheader("월별 자산 평가액 테이블")
    display_df = grouped_df.copy()
    for col in ['연금', '비연금', '합계']:
        display_df[col] = display_df[col].apply(lambda x: f"{x:,.0f} 원")
    display_df = display_df[['연월_str', '연금', '비연금', '합계']].rename(columns={'연월_str': '연월'})
    st.dataframe(display_df.set_index('연월').sort_index(ascending=False), use_container_width=True)

    # 4. 바차트 생성
    fig = px.bar(grouped_df, x='연월_str', y=['연금', '비연금'],
                 title='월별 자산 평가액 (연금 vs 비연금)',
                 labels={'value': '평가액', 'variable': '구분'},
                 barmode='group')

    # Y축 범위 및 눈금 설정
    y_max = math.ceil(grouped_df['합계'].max() / 10000000) * 10000000
    y_min = 100000000
    y_step = 10000000

    fig.update_layout(
        xaxis_title="연월",
        yaxis_title="평가액 (원)",
        yaxis_tickformat=',d',
        yaxis=dict(
            range=[y_min, y_max],
            tickmode='array',
            tickvals=list(range(y_min, y_max + y_step, y_step)),
            ticktext=[f"{i / 100000000:.1f}억" for i in range(y_min, y_max + y_step, y_step)]
        ),
        xaxis=dict(
            tickmode='linear',
            dtick="M1",
            tickformat="%Y-%m"
        ),
        legend_title_text='구분'
    )

    # 바 위에 값 표시
    for trace in fig.data:
        fig.add_traces(
            px.bar(grouped_df, x='연월_str', y=trace.name,
                   text=grouped_df[trace.name].apply(format_currency)).update_traces(
                textposition='outside',
                textfont_size=10,
                textfont_color='black',
                showlegend=False,
                marker_color='rgba(0,0,0,0)'
            ).data
        )

    st.plotly_chart(fig, use_container_width=True)


# Streamlit 멀티페이지 앱 기능 활용
if __name__ == "__main__":
    if 'data_processor' in st.session_state:
        render(st.session_state['data_processor'])
    else:
        st.error("Please run the main app first to initialize data.")