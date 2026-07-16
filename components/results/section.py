import streamlit as st
from core.scoring import calculate_scores
from core.recommendations import get_recommendations, requires_professional_support
from components.results.result_card import render_result_card
from components.results.charts import render_radar_chart, render_score_bars
from components.results.recommendation_card import render_recommendation_card
from components.assessment.support_notice import render_support_notice
from core.questions import DASS21_QUESTIONS

def _reset(prefix: str):
    for question in DASS21_QUESTIONS:
        st.session_state.pop(
            f"{prefix}_question_{question['id']}",
            None,
        )

    st.session_state.pop(
        f"{prefix}_results_visible",
        None,
    )

    st.rerun()

def render_results(answers: dict, prefix: str = "version2"):
    missing = [str(k) for k,v in answers.items() if v is None]
    if missing:
        st.error("Please answer every question. Missing: " + ", ".join(missing))
        return

    results = calculate_scores(answers)
    st.divider()
    st.header("Your Results")

    cols = st.columns(3)
    for col, scale in zip(cols, ["Depression","Anxiety","Stress"]):
        with col:
            render_result_card(scale, results[scale])

    st.markdown("## Visual Summary")
    left, right = st.columns([1.1,1], gap="large")
    with left:
        render_radar_chart(results)
    with right:
        render_score_bars(results)

    st.divider()
    st.header("Personalized Suggestions")
    recs = get_recommendations(results)
    cols = st.columns(2)
    for i, item in enumerate(recs):
        with cols[i % 2]:
            render_recommendation_card(item)

    if requires_professional_support(results):
        st.warning("One or more scores are severe or extremely severe. Consider speaking with a qualified mental-health professional.")
    else:
        st.info("These results are a screening snapshot, not a diagnosis.")

    render_support_notice()

    if st.button("Start a New Assessment", use_container_width=True):
        _reset(prefix)
