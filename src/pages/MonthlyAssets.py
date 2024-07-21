import streamlit as st
from data.data_processor import DataProcessor
import plotly.figure_factory as ff

def render(data_processor: DataProcessor):
    st.set_page_config(
        layout='wide',
        page_title="월간 자산"
    )
    st.title("월간 자산")

    fig = ff.create_table(data_processor.get_data("monthly_assets"))
    st.plotly_chart(fig, use_container_width=True)

# Streamlit 멀티페이지 앱 기능 활용
if __name__ == "__main__":
    if 'data_processor' in st.session_state:
        render(st.session_state['data_processor'])
    else:
        st.error("Please run the main app first to initialize data.")
