import pandas as pd
import streamlit as st
import plotly.express as px


def view_pension(all_df: dict):
    df = all_df["pension_mp"]

    st.header("연금관리")
    st.dataframe(df)
