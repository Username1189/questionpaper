import streamlit as st
import pandas as pd
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
data = pd.read_csv("Credentials.csv")
student_id = st.text_input("ID: ")
student_password = st.text_input("Password: ")
state = SessionState.get(question_number=0)


def main():
    if not state.started:
        # student_id = st.text_input("ID: ")
        # student_password = st.text_input("Password: ")
        login_cred()
    else:
        question_paper()


def login_cred():
    found = False
    for a in data["ID"]:
        if student_id == a:
            found = True
            break
    if not found:
        st.error("ID Not Found")
        return
    found = False
    for a in data["Password"]:
        if student_password == a:
            found = True
            break
    if not found:
        st.error("Password Invalid!!!")
        return
    i = 0
    for a in data["ID"]:
        if a == student_id:
            if int(data["Done Test"][i]) == 1:
                st.error("You Have Already written the test")
                return
        i += 1
    state.started = True
    raise RerunException(RerunData())


@st.cache
def get_question(question_number):
    q = file["Questions"][question_number]
    ans = file["Ans"][question_number]
    choices = ["Please select an answer", file["A"][question_number], file["B"][question_number],
               file["C"][question_number], file["D"][question_number]]
    return q, ans, choices


def question_paper():
    pages_panel()
    if state.done:
        max_score = 0
        for i in file["CorrectPoints"]:
            max_score += int(i)
        st.subheader(f"Your Score - {state.score}/{max_score}")
        if state.score == max_score:
            st.subheader("Perfect!!!")
        i = 0
        for a in data["ID"]:
            if a == student_id:
                data.loc[i, "Done Test"] = 1
                data.to_csv("Credentials.csv", index=False)
                break
            i += 1
        print(data)
        print(student_id)
        return "DONE"

    q, ans, choices = get_question(state.question_number)

    st.header(q)
    options = st.radio('Answer:', choices)

    col = st.columns(9)
    button = False
    button2 = False
    if not state.question_number == 0:
        button2 = col[0].button("Back")
    if not state.hidden:
        button = col[1].button("Next")

    if button2:
        state.question_number -= 1
        raise RerunException(RerunData())

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


def pages_panel():
    col = st.sidebar.columns(7)
    i = 0
    for a in range(len(file["Questions"])):
        if col[i].button(str(a + 1)):
            state.question_number = a
        i += 1
        if i == len(col):
            i = 0


if __name__ == '__main__':
    main()
