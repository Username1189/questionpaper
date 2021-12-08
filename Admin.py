import streamlit as st
import pandas as pd


@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


class Admin:
    def __init__(self):
        self.resultsDF = pd.read_csv("Results.csv")

    def show(self):
        csv = convert_df(self.resultsDF)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Results.csv',
            mime='text/csv')
        if st.button("Clear results"):
            empty = {"ID": [], "Score": []}
            pd.DataFrame.from_dict(empty).to_csv("Results.csv")
        if st.button("Create New Test"):
            st.file_uploader("Test Questions", "text/csv")
