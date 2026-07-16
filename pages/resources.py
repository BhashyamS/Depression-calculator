import streamlit as st
from components.ui.styles import load_styles
from components.layout.footer import render_footer

load_styles()
st.title("Support Resources")
st.write("Use this page to provide local and national support information.")
st.markdown("""
### United States
- Call or text **988** for the Suicide & Crisis Lifeline.
- Call **911** for immediate danger or a medical emergency.

### General
- Contact a licensed therapist, counselor, psychologist, psychiatrist, or primary-care provider.
- Reach out to someone you trust when symptoms feel difficult or isolating.
""")
render_footer()
