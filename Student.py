import SessionState
from Question import Question
from Admin import Admin
import streamlit as st
import pandas as pd
from streamlit.script_runner import RerunException
from streamlit.script_request_queue import RerunData


class Student:
    def __init__(self):
        st.markdown(
            """ <style>
                    div[role="radiogroup"] >  :first-child{
                        display: none !important;
                    }
                </style>
                """, True)
        # file = pd.read_csv("Questions.csv")
        self.data = pd.read_csv("Credentials.csv")
        self.results = None
        self.resultsfile = None
        self.resultsDF = None
        self.state = SessionState.get(question_number=0)
        self.questions = {}
        for a in range(len(self.state.file["Questions"])):
            self.questions[a] = Question(self.state)
        if self.state.showIDPass:
            self.state.student_id = st.text_input("ID: ")
            self.state.student_password = st.text_input("Password: ")

    def show(self):
        if not self.state.started:
            # student_id = st.text_input("ID: ")
            # student_password = st.text_input("Password: ")
            self.login_cred()
        else:
            if self.state.showIDPass:
                self.state.showIDPass = False
                raise RerunException(RerunData())
            self.question_paper()

    def login_cred(self):
        if self.state.student_id == "" or self.state.student_password == "":
            return
        if self.state.student_id == "admin" and self.state.student_password == "admin":
            admin = Admin()
            admin.show()
            return "ADMIN"
        found = False
        for a in self.data["ID"]:
            if self.state.student_id == a:
                found = True
                break
        if not found:
            st.error("ID Not Found")
            return "A"
        found = False
        for a in self.data["Password"]:
            if self.state.student_password == a:
                found = True
                break
        if not found:
            st.error("Password Invalid!!!")
            return "A"
        i = 0
        for a in self.data["ID"]:
            if a == self.state.student_id:
                if int(self.data["Done Test"][i]) == 1:
                    st.error("You Have Already written the test")
                    return "A"
            i += 1
        self.state.started = True
        raise RerunException(RerunData())

    def calc_tot_score(self):
        score = 0
        for question_number, ans in self.state.answers.items():
            if ans != ["asdfghjkl"] and ans != []:
                correct = True
                for a in ans:
                    if str(self.state.correctAns[question_number]).find(a) == -1:
                        correct = False
                        break
                if correct:
                    score += self.state.correctPoints[question_number]
                else:
                    score += self.state.wrongPoints[question_number]
        # score = 0
        # i = 0
        # for question_number, ans in self.state.answers.items():
        #     if self.state.correctAns[question_number] == ans:
        #         score += self.state.correctPoints[i]
        #     elif ans == "asdfghjkl":
        #         pass
        #     else:
        #         score += self.state.wrongPoints[i]
        #     i += 1

        return score

    def question_paper(self):
        self.pages_panel()
        if self.state.done:
            max_score = 0
            for i in self.state.file["CorrectPoints"]:
                max_score += int(i)
            score = self.calc_tot_score()
            st.subheader(f"Your Score : {score}/{max_score}")

            self.resultsfile = pd.read_csv("Results.csv")
            self.results = {"ID": [], "Score": []}
            for i in self.resultsfile["ID"]:
                self.results["ID"].append(i)
            for i in self.resultsfile["Score"]:
                self.results["Score"].append(i)
            self.results["ID"].append(self.state.student_id)
            self.results["Score"].append(score)
            self.resultsDF = pd.DataFrame.from_dict(self.results)
            self.resultsDF.to_csv("Results.csv", index=False)

            i = 0
            for a in self.data["ID"]:
                if a == self.state.student_id:
                    self.data.loc[i, "Done Test"] += 1
                    self.data.to_csv("Credentials.csv", index=False)
                    break
                i += 1
            return "DONE"

        question = self.questions[self.state.question_number]

        col1, col2 = st.columns(2)
        col1.header(question.q)
        # mark = col2.checkbox("Mark For Review")
        # self.state.markedForReview[self.state.question_number] = mark
        if self.state.question_number in self.state.answers:
            i = 0
            for a in question.choices:
                if a == self.state.answers[self.state.question_number]:
                    break
                i += 1
            if self.state.file["MultipleAnswers"][self.state.question_number].lower() == "yes":
                options = []
                for j in range(1, 5):
                    cond = False
                    if j == i:
                        cond = st.checkbox(question.choices[j], True, key=j)
                    else:
                        cond = st.checkbox(question.choices[j], key=j)
                    if cond:
                        options.append(question.choices[j])
            else:
                options = [st.radio('Answer:', question.choices, i)]
        else:
            if self.state.file["MultipleAnswers"][self.state.question_number].lower() == "yes":
                options = []
                for j in range(1, 5):
                    if st.checkbox(question.choices[j], key=j):
                        options.append(question.choices[j])
            else:
                options = [st.radio('Answer:', question.choices)]

        col = st.columns(9)
        forward_button = False
        back_button = False
        if not self.state.question_number == 0:
            back_button = col[0].button("Back")
        if not self.state.question_number == len(self.state.file["Questions"]):
            forward_button = col[1].button("Save&Next")

        if back_button:
            self.state.question_number -= 1
            raise RerunException(RerunData())

        if forward_button:
            self.state.submitted_answer(options, question.ans)
            self.state.done_question()
            if self.state.question_number == len(self.state.file["Questions"]) - 1:
                self.state.done = True
                raise RerunException(RerunData())
            self.state.question_number += 1

            raise RerunException(RerunData())  # widget_state=None

    def pages_panel(self):
        col = st.sidebar.columns(7)
        i = 0
        for a in range(len(self.state.file["Questions"])):
            if col[i].button(str(a + 1)):
                self.state.question_number = a
            i += 1
            if i == len(col):
                i = 0
