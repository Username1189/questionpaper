import streamlit as st
from PIL import Image
from Student import Student


def main():
    st.set_page_config("MCQ question paper", "chart_with_upwards_trend")
    student = Student()
    student.show()


if __name__ == '__main__':
    main()
