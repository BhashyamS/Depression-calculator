import streamlit as st
from components.ui.styles import load_styles
from components.layout.footer import render_footer

load_styles()

st.markdown("""
<div class="hero">
    <div class="assessment-badge">MindSense</div>
    <h1>A calmer way to check in with yourself.</h1>
    <p class="assessment-subtitle">
        Explore symptoms related to depression, anxiety, and stress through a private DASS-21 self-assessment.
    </p>
</div>
""", unsafe_allow_html=True)

left, center, right = st.columns([1,1.4,1])
with center:
    if st.button("Start Version 2", use_container_width=True):
        st.switch_page("pages/version_2.py")

st.markdown("## Explore the versions")
c1,c2,c3 = st.columns(3)
with c1:
    st.markdown("### Version 1")
    st.write("Original full-page questionnaire and score output.")
    if st.button("Open Version 1", use_container_width=True):
        st.switch_page("pages/version_1.py")
with c2:
    st.markdown("### Version 2")
    st.write("Calmer design, horizontal responses, charts, and recommendations.")
    if st.button("Open Version 2", use_container_width=True):
        st.switch_page("pages/version_2.py")
with c3:
    st.markdown("### Version 3")
    st.write("Prototype for recurring check-ins and trend tracking.")
    if st.button("Open Version 3", use_container_width=True):
        st.switch_page("pages/version_3.py")

render_footer()
