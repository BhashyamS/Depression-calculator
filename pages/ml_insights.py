import json
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.layout.footer import render_footer
from components.ui.styles import load_styles
from ml.anomaly_detection import detect_large_changes
from ml.predictor import MODEL_PATH, predict_next_week

METRICS_PATH = Path("models/model_metrics.json")

load_styles()
st.title("Machine Learning Insights")
st.caption("Experimental next-week score forecasting")

st.warning(
    "This model is trained on synthetic demonstration data. "
    "It is not a diagnosis or clinical prediction."
)

if not MODEL_PATH.exists():
    st.error(
        "The model is missing. Run:\n\n"
        "`python -m ml.generate_demo_data`\n\n"
        "`python -m ml.train_models`"
    )
    st.stop()

st.markdown("## Current weekly check-in")

c1, c2, c3 = st.columns(3)
with c1:
    depression_score = st.slider("Current depression score", 0, 42, 12)
with c2:
    anxiety_score = st.slider("Current anxiety score", 0, 42, 10)
with c3:
    stress_score = st.slider("Current stress score", 0, 42, 16)

st.markdown("## Wellness factors")

c1, c2, c3 = st.columns(3)
with c1:
    sleep_quality = st.slider("Sleep quality", 1, 5, 3)
    exercise_days = st.slider("Exercise days this week", 0, 7, 3)
with c2:
    mood_rating = st.slider("Overall mood", 1, 10, 6)
    stressful_events = st.slider("Stressful events this week", 0, 5, 1)
with c3:
    social_connection = st.slider("Social connection", 1, 5, 3)
    week = st.number_input("Check-in week", 1, 52, 5)

if st.button("Generate Next-Week Forecast", type="primary", use_container_width=True):
    features = {
        "depression_score": depression_score,
        "anxiety_score": anxiety_score,
        "stress_score": stress_score,
        "sleep_quality": sleep_quality,
        "exercise_days": exercise_days,
        "mood_rating": mood_rating,
        "stressful_events": stressful_events,
        "social_connection": social_connection,
        "week": week,
    }

    predictions = predict_next_week(features)
    current_scores = {
        "Depression": depression_score,
        "Anxiety": anxiety_score,
        "Stress": stress_score,
    }

    st.divider()
    st.header("Experimental Forecast")

    cols = st.columns(3)
    for col, scale in zip(cols, ["Depression", "Anxiety", "Stress"]):
        with col:
            change = predictions[scale] - current_scores[scale]
            st.metric(
                f"Predicted {scale}",
                f"{predictions[scale]:.1f}",
                f"{change:+.1f}",
                delta_color="inverse",
            )

    comparison = pd.DataFrame({
        "Scale": ["Depression", "Anxiety", "Stress"],
        "Current": [depression_score, anxiety_score, stress_score],
        "Predicted next week": [
            predictions["Depression"],
            predictions["Anxiety"],
            predictions["Stress"],
        ],
    })

    figure = go.Figure()
    figure.add_bar(name="Current", x=comparison["Scale"], y=comparison["Current"])
    figure.add_bar(
        name="Predicted next week",
        x=comparison["Scale"],
        y=comparison["Predicted next week"],
    )
    figure.update_layout(
        barmode="group",
        height=420,
        yaxis_title="DASS-21 score",
        yaxis_range=[0, 42],
        margin={"l": 30, "r": 30, "t": 40, "b": 30},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.72)",
        legend={"orientation": "h"},
    )
    st.plotly_chart(
        figure,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    alerts = detect_large_changes(current_scores, predictions)
    if alerts:
        st.warning(" ".join(alerts))

    st.info(
        "These predictions are experimental estimates from synthetic data."
    )

if METRICS_PATH.exists():
    st.divider()
    st.markdown("## Model evaluation")
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    rows = []
    for target, values in metrics.items():
        rows.append({
            "Target": target.replace("next_", "").replace("_score", "").title(),
            "MAE": values["mae"],
            "R²": values["r2"],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

render_footer()
