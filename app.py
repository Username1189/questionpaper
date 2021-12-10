import streamlit as st
from Student import Student


def main():
    st.set_page_config(page_title="MCQ question paper")
    st.markdown(""" <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)
    Student().show()


if __name__ == '__main__':
    main()
