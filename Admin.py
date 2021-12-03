import streamlit as st
import pandas as pd


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


class Admin:
    def __init__(self):
        self.resultsDF = pd.read_csv("Results.csv")

    def show(self):
        csv = convert_df(self.resultsDF)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='results.csv',
            mime='text/csv')
