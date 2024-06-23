import streamlit as st
import plotly.express as px

class BarChartView:
    @staticmethod
    def display(data):
        fig = px.bar(data, x='yyyymm', y='count')
        st.plotly_chart(fig)