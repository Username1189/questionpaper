import streamlit as st
import pandas as pd
import numpy as np
import SessionState
from streamlit.script_runner import RerunException
from streamlit.script_request_queue import RerunData

# st.set_option('browser.serverAddress', 'localhost')
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """, True)
file = pd.read_csv("Questions.csv")
state = SessionState.get(question_number=0)


def main():
    question_paper()

@st.cache
def get_question(question_number):
    q = file["Questions"][question_number]
    ans = file["Ans"][question_number]
    choices = ["Please select an answer", file["A"][question_number], file["B"][question_number],
               file["C"][question_number], file["D"][question_number]]
    return q, ans, choices


def question_paper():
    if state.done:
        max_score = 0
        for i in file["CorrectPoints"]:
            max_score += int(i)
        st.subheader(f"Your Score - {state.score}/{max_score}")
        if state.score == max_score:
            st.subheader("Perfect!!!")
        return "DONE"

    q, ans, choices = get_question(state.question_number)

    st.header(q)
    options = st.radio('Answer:', choices)

    button = False
    if not state.hidden:
        button = st.button("Next")

    if button:
        st.write(f"You chose {options}")
        if ans == options:
            if state.question_number not in state.questionsDone:
                state.submittedAnswer(file["CorrectPoints"][state.question_number])
        else:
            state.submittedAnswer(file["WrongPoints"][state.question_number])
        state.done_question()
        if state.question_number == len(file["Questions"]) - 1:
            state.done = True
            st.write(state.score)
            raise RerunException(RerunData())
        state.question_number += 1
        if state.question_number == len(file["Questions"]):
            state.hidden = True

        raise RerunException(RerunData())  # widget_state=None


if __name__ == '__main__':
    main()
