import streamlit as st
import pandas as pd
import plotly.express as px
from services.config import Config
from repositories.data_repository import DataRepository


def view_accounts(config: Config, repository: DataRepository):
    db_name = config['data_source']['spreadsheet_name']
    table_name = config['tables']['accounts']
    df = repository.get_all_data(db_name, table_name)

    # Header
    st.header("계좌 현황")
    st.dataframe(df)
