import streamlit as st
from Student import Student


def main():
    st.set_page_config(page_title="MCQ question paper")
    student = Student()
    student.show()


if __name__ == '__main__':
    main()
