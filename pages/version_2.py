import streamlit as st

from components.ui.styles import load_styles
from components.assessment.header import render_header
from components.assessment.progress import render_progress
from components.assessment.form import render_form
from components.results.section import render_results
from components.layout.footer import render_footer


load_styles()
render_header()

results_visible = st.session_state.get("version2_results_visible", False)

if not results_visible:
    render_progress("version2")

answers, submitted = render_form("version2")

if submitted:
    missing_answers = any(answer is None for answer in answers.values())

    if not missing_answers:
        st.session_state["version2_results_visible"] = True
        st.rerun()
    else:
        render_results(answers, "version2")

elif results_visible:
    render_results(answers, "version2")

render_footer()