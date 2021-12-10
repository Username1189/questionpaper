import streamlit as st
from streamlit.script_runner import RerunException
from streamlit.script_request_queue import RerunData
import SessionState
import pandas as pd

st.markdown(
            """ <style>
                    div[role="radiogroup"] >  :first-child{
                        display: none !important;
                    }
                </style>
                """, True)

state = SessionState.get()
data = pd.read_csv('Credentials.csv')

def login_cred():
    if state.student_id == "" or state.student_password == "":
        return
    if state.student_id == "admin" and state.student_password == "admin":
        admin = admin()
        admin.show()
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
        correctAns = str(state.file["Ans"][i]).split(",")
        correctAns.sort()
        a = False
        try:
            asdfghjkl = state.answers[i]
        except KeyError:
            a = True
        if not a:
            if correctAns == state.answers[i]:
                score += state.file["CorrectPoints"][i]
            elif state.answers[i] == [] or state.answers[i] == "DONTSHOW":
                pass
            else:
                score += state.file["WrongPoints"][i]
    return score

def question_paper():
    if state.done:
        st.balloons()
        st.header("Score: " + str(calc_score()))
        resultsDict = {"ID": [], "Score": []}
        results = pd.read_csv('Results.csv')
        for a in results["ID"]:
            resultsDict["ID"].append(a)
        for a in results["Score"]:
            resultsDict["Score"].append(a)
        resultsDict["ID"].append(state.student_id)
        resultsDict["Score"].append(calc_score())
        resultsDF = pd.DataFrame.from_dict(resultsDict)
        resultsDF.to_csv("Results.csv", index=False)
        return None
    st.header('Question Paper')
    for i in range(len(state.file['Questions'])):
        st.subheader(str(i+1) + ". " + state.file['Questions'][i])
        if str(state.file['Ans'][i]).find(',') != -1:
            selectedAns = []
            choiceNames = ['A', 'B', 'C', 'D']
            for j in range(4):
                if st.checkbox(str(state.file[choiceNames[j]][i]), key=str(j)+str(i)):
                    selectedAns.append(str(state.file[choiceNames[j]][i]))
            selectedAns.sort()
            state.answers[i] = selectedAns
        else:
            selectedAns = [st.radio("Answer:", ["DONTSHOW", state.file['A'][i], state.file['B'][i], state.file['C'][i], state.file['D'][i]])]
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
