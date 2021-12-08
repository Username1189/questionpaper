"""Hack to add per-session state to Streamlit.

Usage
-----

>>> import SessionState
>>>
>>> session_state = SessionState.get(user_name='', favorite_color='black')
>>> session_state.user_name
''
>>> session_state.user_name = 'Mary'
>>> session_state.favorite_color
'black'

Since you set user_name above, next time your script runs this will be the
result:
>>> session_state = get(user_name='', favorite_color='black')
>>> session_state.user_name
'Mary'

"""
import streamlit.report_thread as ReportThread
import pandas as pd
from streamlit.server.server import Server


class SessionState(object):
    def __init__(self, **kwargs):
        """A new SessionState object.

        Parameters
        ----------
        **kwargs : any
            Default values for the session state.

        Example
        -------
        >>> session_state = SessionState(user_name='', favorite_color='black')
        >>> session_state.user_name = 'Mary'
        ''
        >>> session_state.favorite_color
        'black'

        """
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.file = pd.read_csv("Questions.csv")
        self.totalScore = 0
        self.questionsDone = []
        self.started = False
        self.hidden = False
        self.done = False
        self.showIDPass = True
        self.student_id = None
        self.student_password = None
        self.correctAns = {}
        self.correctPoints = {}
        self.wrongPoints = {}
        self.answers = {}
        self.markedForReview = {}

    def submitted_answer(self, answer, correct_ans):
        correct_points = self.file["CorrectPoints"][self.question_number]
        wrong_points = self.file["WrongPoints"][self.question_number]
        if answer == ["Please select an answer"]:
            self.answers[self.question_number] = ["asdfghjkl"]
        else:
            self.answers[self.question_number] = answer
        self.correctAns[self.question_number] = correct_ans
        self.correctPoints[self.question_number] = correct_points
        self.wrongPoints[self.question_number] = wrong_points

    def done_question(self):
        self.questionsDone.append(self.question_number)


def get(**kwargs):
    """Gets a SessionState object for the current session.

    Creates a new object if necessary.

    Parameters
    ----------
    **kwargs : any
        Default values you want to add to the session state, if we're creating a
        new one.

    Example
    -------
    >>> session_state = get(user_name='', favorite_color='black')
    >>> session_state.user_name
    ''
    >>> session_state.user_name = 'Mary'
    >>> session_state.favorite_color
    'black'

    Since you set user_name above, next time your script runs this will be the
    result:
    >>> session_state = get(user_name='', favorite_color='black')
    >>> session_state.user_name
    'Mary'

    """
    # Hack to get the session object from Streamlit.

    ctx = ReportThread.get_report_ctx()

    this_session = None

    current_server = Server.get_current()
    if hasattr(current_server, "_session_infos"):
        # Streamlit < 0.56
        session_infos = Server.get_current()._session_infos.values()
    else:
        session_infos = Server.get_current()._session_info_by_id.values()

    # for session_info in session_infos:
    #     s = session_info.session
    #     # if (
    #     #     # Streamlit < 0.54.0
    #     #     (hasattr(s, "_main_dg") and s._main_dg == ctx.main_dg)
    #     #     or
    #     #     # Streamlit >= 0.54.0
    #     #     (not hasattr(s, "_main_dg") and s.enqueue == ctx.enqueue)
    #     # ):
    #     this_session = s

    for session_info in session_infos:
        s = session_info.session
        if s.id == ctx.session_id:
            this_session = s

    # if this_session is None:
    #     raise RuntimeError(
    #         "Oh noes. Couldn't get your Streamlit Session object"
    #         "Are you doing something fancy with threads?"
    #     )

    # Got the session object! Now let's attach some state into it.

    if not hasattr(this_session, "_custom_session_state"):
        this_session._custom_session_state = SessionState(**kwargs)

    return this_session._custom_session_state
