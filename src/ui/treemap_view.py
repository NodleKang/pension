import streamlit as st
import plotly.express as px

class TreemapView:
    @staticmethod
    def display(data, value_column, color_column):
        fig = px.treemap(data, path=['yyyymm', 'code'], values=value_column, color=color_column)
        st.plotly_chart(fig)