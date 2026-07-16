import streamlit as st
from components.ui.styles import load_styles
from components.layout.footer import render_footer

load_styles()
st.title("About DASS-21")
st.write("""
The DASS-21 is a 21-item self-report questionnaire with three seven-item subscales:
Depression, Anxiety, and Stress. Each response is scored from 0 to 3, and each subscale
sum is multiplied by two for comparison with conventional severity ranges.
""")
st.warning("The DASS-21 is not a diagnostic test and does not assess immediate safety or suicidal thoughts.")
render_footer()
