import streamlit as st
from core.questions import RESPONSE_OPTIONS

CATEGORY_STYLES = {
    "Depression": ("🌤️", "#F3EDFA", "#6F5A8A"),
    "Anxiety": ("🫧", "#EAF5FA", "#4F7485"),
    "Stress": ("🌿", "#EAF4EE", "#557563"),
}

def render_question(question: dict, key_prefix: str) -> int | None:
    icon, bg, text = CATEGORY_STYLES[question["category"]]
    st.markdown(f"""
    <div class="question-card">
        <div class="question-card-top">
            <div class="question-number">Question {question['id']} of 21</div>
            <div class="question-category" style="background:{bg};color:{text};">
                {icon} {question['category']}
            </div>
        </div>
        <div class="question-text">{question['text']}</div>
    </div>
    """, unsafe_allow_html=True)

    return st.radio(
        f"Response for question {question['id']}",
        options=list(RESPONSE_OPTIONS),
        format_func=lambda value: RESPONSE_OPTIONS[value],
        horizontal=True,
        index=None,
        key=f"{key_prefix}_question_{question['id']}",
        label_visibility="collapsed",
    )
