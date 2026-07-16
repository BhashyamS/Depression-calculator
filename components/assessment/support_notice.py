import streamlit as st

def render_support_notice():
    st.markdown("""
    <div class="safety-card">
        <div class="safety-title">Immediate support</div>
        <div class="safety-text">
            The DASS-21 does not assess suicidal thoughts or immediate danger.
            If you may hurt yourself or someone else, contact emergency services.
            In the United States, call or text <strong>988</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)
