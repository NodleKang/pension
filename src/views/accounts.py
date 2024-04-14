import streamlit as st
import plotly.figure_factory as ff


def view_accounts(all_df: dict):
    df = all_df["accounts"]

    st.header("계좌 현황")
    fig = ff.create_table(df)
    st.plotly_chart(fig, use_container_width=True)
