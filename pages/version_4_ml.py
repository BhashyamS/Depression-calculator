import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout.footer import render_footer
from components.ui.styles import load_styles
from ml_v4.predictor import MODEL_PATH, predict_risk


METRICS_PATH = Path("models/mindsense_risk_metrics.json")
IMPORTANCE_PATH = Path(
    "models/mindsense_risk_feature_importance.csv"
)

load_styles()

st.title("Interactive ML Insights — Version 4")
st.caption(
    "Random Forest classification using DASS-21 scores and wellness factors"
)

st.warning(
    "This machine-learning feature is trained on synthetic demonstration "
    "data. It is not a diagnosis, a clinical prediction, or medical advice."
)

with st.expander("How this differs from the DASS-21 result"):
    st.markdown(
        """
        - **DASS-21 scoring** uses the official fixed scoring rules.
        - **ML Insights** combines those scores with lifestyle factors.
        - The model demonstrates preprocessing, training, prediction,
          probability output, evaluation, and feature importance.
        """
    )

if not MODEL_PATH.exists():
    st.error(
        "The trained model is missing. Run these commands from the project folder:\n\n"
        "`python -m ml_v4.generate_training_data`\n\n"
        "`python -m ml_v4.train_model`"
    )
    st.stop()

st.markdown("## DASS-21 scores")

score_col1, score_col2, score_col3 = st.columns(3)

with score_col1:
    depression_score = st.slider(
        "Depression score",
        min_value=0,
        max_value=42,
        value=12,
    )

with score_col2:
    anxiety_score = st.slider(
        "Anxiety score",
        min_value=0,
        max_value=42,
        value=10,
    )

with score_col3:
    stress_score = st.slider(
        "Stress score",
        min_value=0,
        max_value=42,
        value=16,
    )

st.markdown("## Lifestyle and wellness factors")

left, middle, right = st.columns(3)

with left:
    sleep_hours = st.slider(
        "Average sleep hours",
        min_value=3.0,
        max_value=11.0,
        value=7.0,
        step=0.5,
    )

    sleep_quality = st.slider(
        "Sleep quality",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = very poor, 5 = very good",
    )

with middle:
    exercise_days = st.slider(
        "Exercise days per week",
        min_value=0,
        max_value=7,
        value=3,
    )

    social_support = st.slider(
        "Social support",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = very limited, 5 = very strong",
    )

with right:
    mood_rating = st.slider(
        "Overall mood",
        min_value=1,
        max_value=10,
        value=6,
        help="1 = very low, 10 = very positive",
    )

    stressful_events = st.slider(
        "Stressful events this week",
        min_value=0,
        max_value=5,
        value=1,
    )

work_study_hours = st.slider(
    "Work or study hours per week",
    min_value=0,
    max_value=90,
    value=40,
)

if st.button(
    "Generate ML Insight",
    type="primary",
    use_container_width=True,
):
    features = {
        "depression_score": depression_score,
        "anxiety_score": anxiety_score,
        "stress_score": stress_score,
        "sleep_hours": sleep_hours,
        "sleep_quality": sleep_quality,
        "exercise_days": exercise_days,
        "social_support": social_support,
        "mood_rating": mood_rating,
        "work_study_hours": work_study_hours,
        "stressful_events": stressful_events,
    }

    result = predict_risk(features)
    probability_percent = result["probability"] * 100

    st.divider()
    st.header("Experimental ML Result")

    result_col1, result_col2 = st.columns([1, 1.4])

    with result_col1:
        st.metric(
            "Elevated-pattern probability",
            f"{probability_percent:.1f}%",
        )
        st.markdown(f"### {result['label']}")

    with result_col2:
        st.progress(result["probability"])

        if probability_percent >= 70:
            st.warning(
                "The model found a stronger elevated-risk pattern in the "
                "selected inputs."
            )
        elif probability_percent >= 40:
            st.info(
                "The model found a mixed pattern in the selected inputs."
            )
        else:
            st.success(
                "The model found a lower-risk pattern in the selected inputs."
            )

    st.caption(
        "This percentage describes the model's synthetic training target. "
        "It is not the probability that a person has depression."
    )

if METRICS_PATH.exists():
    st.divider()
    st.markdown("## Model Evaluation")

    metrics = json.loads(
        METRICS_PATH.read_text(encoding="utf-8")
    )

    columns = st.columns(5)

    for column, label, key in zip(
        columns,
        ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        ["accuracy", "precision", "recall", "f1", "roc_auc"],
    ):
        with column:
            st.metric(label, f"{metrics[key]:.3f}")

    st.caption(
        f"Training rows: {metrics['training_rows']:,} · "
        f"Test rows: {metrics['test_rows']:,} · "
        f"Data: {metrics['data_type']}"
    )

if IMPORTANCE_PATH.exists():
    st.divider()
    st.markdown("## Feature Importance")

    importance = pd.read_csv(IMPORTANCE_PATH)

    figure = px.bar(
        importance.sort_values("importance"),
        x="importance",
        y="feature",
        orientation="h",
        labels={
            "importance": "Random Forest importance",
            "feature": "Feature",
        },
    )

    figure.update_layout(
        height=500,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.72)",
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={"displayModeBar": False},
    )

render_footer()
