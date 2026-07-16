import streamlit as st

from core.questions import DASS21_QUESTIONS


def render_progress(prefix: str) -> int:
    total_questions = len(DASS21_QUESTIONS)

    answered = sum(
        st.session_state.get(
            f"{prefix}_question_{question['id']}"
        )
        is not None
        for question in DASS21_QUESTIONS
    )

    percentage = round((answered / total_questions) * 100)

    progress_html = (
        '<div class="fixed-progress-wrapper">'
        '<div class="fixed-progress-content">'
        '<div class="fixed-progress-title">Progress Bar</div>'
        '<div class="fixed-progress-row">'
        '<div class="fixed-progress-track">'
        f'<div class="fixed-progress-fill" style="width:{percentage}%;"></div>'
        '</div>'
        f'<div class="fixed-progress-percentage">{percentage}%</div>'
        '</div>'
        f'<div class="fixed-progress-count">'
        f'{answered} of {total_questions} questions completed'
        '</div>'
        '</div>'
        '</div>'
        '<div class="fixed-progress-spacer"></div>'
    )

    st.markdown(
        progress_html,
        unsafe_allow_html=True,
    )

    return answered