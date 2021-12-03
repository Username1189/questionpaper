import streamlit as st
import random


def get_random_options(a, b, c, d):
    a = random.sample([a, b, c, d], 4)
    return a


class Question:
    def __init__(self, state):
        self.state = state
        self.q, self.ans, self.choices = self.get_question(state.question_number)

    @st.cache
    def get_question(self, question_number):
        q = self.state.file["Questions"][question_number]
        ans = self.state.file["Ans"][question_number]
        choices = ["Please select an answer"]
        a = get_random_options(self.state.file["A"][question_number], self.state.file["B"][question_number],
                               self.state.file["C"][question_number], self.state.file["D"][question_number])
        for i in a:
            choices.append(i)

        return q, ans, choices
