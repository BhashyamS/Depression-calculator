import streamlit as st

def render_result_card(title: str, result: dict):
    st.markdown(f"""
    <div class="result-card">
        <div class="result-top">
            <div class="result-title">{title}</div>
            <div class="severity-pill" style="background:{result['color']};">{result['severity']}</div>
        </div>
        <div class="result-score">{result['score']}</div>
        <div class="result-message">{result['message']}</div>
    </div>
    """, unsafe_allow_html=True)
