import streamlit as st
from core.questions import DASS21_QUESTIONS, RESPONSE_OPTIONS
from core.scoring import calculate_scores
from components.ui.styles import load_styles
from components.layout.footer import render_footer

load_styles()
st.title("Classic Assessment — Version 1")
st.write("This preserves the original all-on-one-page experience.")

answers = {}
with st.form("v1_form"):
    for q in DASS21_QUESTIONS:
        answers[q["id"]] = st.radio(
            f"{q['id']}. {q['text']}",
            options=list(RESPONSE_OPTIONS),
            format_func=lambda value: RESPONSE_OPTIONS[value],
            horizontal=True,
            index=None,
            key=f"v1_{q['id']}",
        )
    submitted = st.form_submit_button("Calculate Results", use_container_width=True)

if submitted:
    missing = [str(k) for k,v in answers.items() if v is None]
    if missing:
        st.error("Please answer all questions. Missing: " + ", ".join(missing))
    else:
        results = calculate_scores(answers)
        cols = st.columns(3)
        for col, scale in zip(cols, ["Depression","Anxiety","Stress"]):
            with col:
                st.metric(scale, results[scale]["score"])
                st.write(results[scale]["severity"])

render_footer()
