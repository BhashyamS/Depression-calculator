import streamlit as st

def render_header():
    st.markdown("""
    <div class="assessment-header">
        <div class="assessment-badge">DASS-21 Self Assessment</div>
        <h1>Take a moment to check in with yourself.</h1>
        <div class="assessment-subtitle">
            Answer each statement based on how you felt during the <strong>past week</strong>.<br><br>
            The assessment has <strong>21 questions</strong> and usually takes about <strong>4 minutes</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)
