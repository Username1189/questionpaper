import streamlit as st
from streamlit.script_runner import RerunException
from streamlit.script_request_queue import RerunData
import SessionState
import pandas as pd

st.set_page_config(page_title="MCQ question paper")
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """, True)

state = SessionState.get()
data = pd.read_csv('Credentials.csv')


def admin():
    if st.button("Clear Results"):
        results_dict = {"ID": [], "Score": []}
        results_df = pd.DataFrame.from_dict(results_dict)
        results_df.to_csv("Results.csv", index=False)
    st.download_button("Download Results", pd.read_csv("Results.csv"), "Results.csv", "text/csv")


def login_cred():
    if state.student_id == "" or state.student_password == "":
        return
    if state.student_id == "admin" and state.student_password == "admin":
        admin()
        return "ADMIN"
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
    state.showIDPass = False
    raise RerunException(RerunData())


def calc_score():
    score = 0
    for i in range(len(state.file["Questions"])):
        correct_ans = str(state.file["Ans"][i]).split(",")
        correct_ans.sort()
        a = False
        try:
            state.answers[i] = state.answers[i]
        except KeyError:
            a = True
        if not a:
            if correct_ans == state.answers[i]:
                score += state.file["CorrectPoints"][i]
            elif state.answers[i] == [] or state.answers[i] == "Don't Show This":
                pass
            else:
                score += state.file["WrongPoints"][i]
    return score


def question_paper():
    if state.done:
        st.balloons()
        st.header("Score: " + str(calc_score()))
        results_dict = {"ID": [], "Score": []}
        results = pd.read_csv('Results.csv')
        for a in results["ID"]:
            results_dict["ID"].append(a)
        for a in results["Score"]:
            results_dict["Score"].append(a)
        results_dict["ID"].append(state.student_id)
        results_dict["Score"].append(calc_score())
        results_df = pd.DataFrame.from_dict(results_dict)
        results_df.to_csv("Results.csv", index=False)
        return None
    st.header('Question Paper')
    for i in range(len(state.file['Questions'])):
        st.subheader(str(i + 1) + ". " + state.file['Questions'][i])
        if str(state.file['Ans'][i]).find(',') != -1:
            selected_ans = []
            choice_names = ['A', 'B', 'C', 'D']
            st.write("Answer:")
            for j in range(4):
                if st.checkbox(str(state.file[choice_names[j]][i]), key=str(j) + str(i)):
                    selected_ans.append(str(state.file[choice_names[j]][i]))
            selected_ans.sort()
        else:
            selected_ans = [st.radio("Answer:", ["Don't Show This", state.file['A'][i], state.file['B'][i], state.file['C'][i],
                                          state.file['D'][i]])]
        state.answers[i] = selected_ans
    if st.button('Submit'):
        state.done = True
        raise RerunException(RerunData())


def main():
    if state.showIDPass:
        state.student_id = st.text_input("ID: ")
        state.student_password = st.text_input("Password: ")
    if not state.started:
        login_cred()
    else:
        question_paper()


if __name__ == '__main__':
    main()
