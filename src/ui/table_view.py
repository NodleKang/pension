import streamlit as st

class TableView:
    @staticmethod
    def display(data):
        st.dataframe(data)