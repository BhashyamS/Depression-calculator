import streamlit as st
from core.questions import DASS21_QUESTIONS
from components.assessment.question_card import render_question

def render_form(prefix: str = "version2") -> tuple[dict, bool]:
    answers = {}
    st.markdown("## Assessment")
    st.caption("Select the response that best describes the past week.")

    for question in DASS21_QUESTIONS:
        answers[question["id"]] = render_question(question, prefix)
        st.write("")

    submitted = st.button("Calculate My Results", type="primary", use_container_width=True)
    return answers, submitted
