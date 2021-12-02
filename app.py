import streamlit as st
import pandas as pd
import random
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
# file = pd.read_csv("Questions.csv")
data = pd.read_csv("Credentials.csv")
state = SessionState.get(question_number=0)
if state.showIDPass:
    state.student_id = st.text_input("ID: ")
    state.student_password = st.text_input("Password: ")


def main():
    if not state.started:
        # student_id = st.text_input("ID: ")
        # student_password = st.text_input("Password: ")
        login_cred()
    else:
        state.showIDPass = False
        question_paper()


def login_cred():
    found = False
    for a in data["ID"]:
        if state.student_id == a:
            found = True
            break
    if not found:
        st.error("ID Not Found")
        return "A"
    found = False
    for a in data["Password"]:
        if state.student_password == a:
            found = True
            break
    if not found:
        st.error("Password Invalid!!!")
        return "A"
    i = 0
    for a in data["ID"]:
        if a == state.student_id:
            if int(data["Done Test"][i]) == 1:
                st.error("You Have Already written the test")
                return "A"
        i += 1
    state.started = True
    raise RerunException(RerunData())


def get_random_options(a, b, c, d):
    a = random.sample([a, b, c, d], 4)
    return a


@st.cache
def get_question(question_number):
    q = state.file["Questions"][question_number]
    ans = state.file["Ans"][question_number]
    choices = ["Please select an answer"]
    a = get_random_options(state.file["A"][question_number], state.file["B"][question_number],
                           state.file["C"][question_number], state.file["D"][question_number])
    for i in a:
        choices.append(i)

    return q, ans, choices


def question_paper():
    print(state.answers)
    pages_panel()
    if state.done:
        max_score = 0
        for i in state.file["CorrectPoints"]:
            max_score += int(i)
        st.subheader(f"Your Score - {state.totalScore}/{max_score}")
        if state.totalScore == max_score:
            st.subheader("Perfect!!!")
        i = 0
        for a in data["ID"]:
            if a == state.student_id:
                data.loc[i, "Done Test"] = 1
                data.to_csv("Credentials.csv", index=False)
                break
            i += 1
        print(data)
        print(state.student_id)
        return "DONE"

    q, ans, choices = get_question(state.question_number)

    st.header(q)
    options = st.radio('Answer:', choices)

    col = st.columns(9)
    forward_button = False
    back_button = False
    if not state.hidden:
        forward_button = col[1].button("Next")
    if not state.question_number == 0:
        back_button = col[0].button("Back")

    if back_button:
        state.question_number -= 1
        raise RerunException(RerunData())

    if forward_button:
        st.write(f"You chose {options}")
        if ans == options:
            if state.question_number not in state.questionsDone:
                state.submitted_answer(state.file["CorrectPoints"][state.question_number], options)
        else:
            state.submitted_answer(state.file["WrongPoints"][state.question_number], options)
        state.done_question()
        if state.question_number == len(state.file["Questions"]) - 1:
            state.done = True
            st.write(state.totalScore)
            raise RerunException(RerunData())
        state.question_number += 1
        if state.question_number == len(state.file["Questions"]):
            state.hidden = True

        raise RerunException(RerunData())  # widget_state=None


def pages_panel():
    col = st.sidebar.columns(7)
    i = 0
    for a in range(len(state.file["Questions"])):
        if col[i].button(str(a + 1)):
            state.question_number = a
        i += 1
        if i == len(col):
            i = 0


if __name__ == '__main__':
    main()
