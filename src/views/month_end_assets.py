import streamlit as st
import pandas as pd
import plotly.express as px
from services.config import Config
from repositories.data_repository import DataRepository


def view_month_end_assets(config: Config, repository: DataRepository):
    db_name = config['data_source']['spreadsheet_name']
    table_name = config['tables']['month_end_assets']
    df = repository.get_all_data(db_name, table_name)

    # Header
    st.header("월말 자산")
    st.dataframe(df)

