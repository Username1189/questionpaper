import streamlit as st
import random


def get_random_options(a, b, c, d):
    a = random.sample([a, b, c, d], 4)
    return a


@st.cache
def get_question(state):
    q = str(state.question_number+1) + ". " + state.file["Questions"][state.question_number]
    ans = state.file["Ans"][state.question_number]
    choices = ["Please select an answer"]
    a = get_random_options(state.file["A"][state.question_number],
                           state.file["B"][state.question_number],
                           state.file["C"][state.question_number],
                           state.file["D"][state.question_number])
    for i in a:
        choices.append(str(i))

    return q, ans, choices


class Question:
    def __init__(self, state):
        self.state = state
        self.q, self.ans, self.choices = get_question(self.state)
