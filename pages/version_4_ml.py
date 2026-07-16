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

st.title("AI Wellness Insights — Version 4")

st.caption(
    "An experimental machine-learning interpretation of DASS-21 "
    "scores and lifestyle factors."
)

st.warning(
    "This model was trained on synthetic demonstration data. "
    "It is not clinically validated and cannot diagnose depression, "
    "anxiety, stress, or any other condition."
)

with st.expander("What information does this page provide?"):
    st.markdown(
        """
        The page combines your DASS-21 scores with wellness factors such
        as sleep, exercise, mood, social support, workload, and recent
        stressful events.

        The model then answers three questions:

        1. **What general pattern did the model identify?**
        2. **Which inputs pushed the result higher or lower?**
        3. **Which wellness areas may be worth paying attention to?**

        The output describes similarity to patterns in synthetic training
        data. It is not the probability that you have depression.
        """
    )


if not MODEL_PATH.exists():
    st.error(
        "The trained model is missing. Run these commands from the "
        "project folder:\n\n"
        "`python -m ml_v4.generate_training_data`\n\n"
        "`python -m ml_v4.train_model`"
    )
    st.stop()


# ============================================================
# User inputs
# ============================================================

st.markdown("## 1. Enter your DASS-21 scores")

st.caption(
    "You can copy these scores from Version 1 or Version 2."
)

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


st.markdown("## 2. Add wellness factors")

left, middle, right = st.columns(3)

with left:
    sleep_hours = st.slider(
        "Average sleep per night",
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


# ============================================================
# Prediction
# ============================================================

if st.button(
    "Generate AI Wellness Insight",
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
    explanations = result["explanations"]

    st.divider()
    st.header("Your AI Wellness Insight")

    result_left, result_right = st.columns(
        [1, 1.5],
        gap="large",
    )

    with result_left:
        st.metric(
            "Model pattern score",
            f"{probability_percent:.1f}%",
        )

        st.markdown(
            f"### {result['concern_level']}"
        )

    with result_right:
        st.progress(result["probability"])

        if probability_percent >= 70:
            st.warning(
                "The selected inputs strongly resemble the model's "
                "elevated-pattern examples."
            )
        elif probability_percent >= 40:
            st.info(
                "The selected inputs contain a mixture of lower- and "
                "higher-concern patterns."
            )
        else:
            st.success(
                "The selected inputs more closely resemble the model's "
                "lower-concern examples."
            )

    st.caption(
        "The percentage is a model classification score. It is not the "
        "probability that you have depression."
    )


    # ============================================================
    # Human-readable summary
    # ============================================================

    st.markdown("## What this means")

    positive_factors = [
        item
        for item in explanations
        if item["contribution"] > 0.01
    ]

    protective_factors = [
        item
        for item in explanations
        if item["contribution"] < -0.01
    ]

    if positive_factors:
        strongest_positive = positive_factors[0]

        st.write(
            f"The strongest factor increasing the model score was "
            f"**{strongest_positive['label']}**."
        )

    if protective_factors:
        strongest_protective = protective_factors[0]

        st.write(
            f"The strongest factor reducing the model score was "
            f"**{strongest_protective['label']}**."
        )

    st.write(
        "The model evaluates all inputs together, so no individual factor "
        "should be interpreted as a cause."
    )


    # ============================================================
    # Local feature explanations
    # ============================================================

    st.markdown("## Factors influencing this result")

    explanation_rows = []

    for item in explanations:
        direction_label = (
            "Raised score"
            if item["contribution"] > 0
            else "Lowered score"
            if item["contribution"] < 0
            else "Minimal effect"
        )

        explanation_rows.append(
            {
                "Factor": item["label"],
                "Your value": item["value"],
                "Comparison value": item["baseline"],
                "Effect": direction_label,
                "Estimated impact": round(
                    item["percentage_points"],
                    1,
                ),
            }
        )

    explanation_frame = pd.DataFrame(explanation_rows)

    chart_frame = explanation_frame.copy()

    figure = px.bar(
        chart_frame.sort_values("Estimated impact"),
        x="Estimated impact",
        y="Factor",
        orientation="h",
        labels={
            "Estimated impact": (
                "Estimated probability change "
                "(percentage points)"
            ),
            "Factor": "Input factor",
        },
    )

    figure.add_vline(
        x=0,
        line_width=1,
        line_dash="dash",
    )

    figure.update_layout(
        height=520,
        margin={
            "l": 20,
            "r": 20,
            "t": 20,
            "b": 20,
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.72)",
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )

    st.caption(
        "Positive values pushed the model score upward. Negative values "
        "pushed it downward. These are model explanations, not proof of "
        "cause and effect."
    )

    with st.expander("View detailed factor table"):
        st.dataframe(
            explanation_frame,
            use_container_width=True,
            hide_index=True,
        )


    # ============================================================
    # Actionable focus areas
    # ============================================================

    st.markdown("## Suggested focus areas")

    recommendations = []

    if sleep_hours < 7 or sleep_quality <= 2:
        recommendations.append(
            (
                "Sleep",
                "Consider working toward a more consistent sleep schedule "
                "and improving sleep quality.",
            )
        )

    if exercise_days < 3:
        recommendations.append(
            (
                "Physical activity",
                "Consider adding manageable movement or exercise during "
                "the week.",
            )
        )

    if social_support <= 2:
        recommendations.append(
            (
                "Social connection",
                "Consider reaching out to someone you trust or finding "
                "supportive social activities.",
            )
        )

    if mood_rating <= 4:
        recommendations.append(
            (
                "Mood support",
                "Low mood may be worth discussing with a qualified "
                "mental-health or healthcare professional.",
            )
        )

    if stressful_events >= 3:
        recommendations.append(
            (
                "Stress management",
                "Consider identifying which current stressors can be "
                "reduced, postponed, delegated, or discussed.",
            )
        )

    if work_study_hours >= 60:
        recommendations.append(
            (
                "Workload",
                "A high weekly workload may leave limited time for rest "
                "and recovery.",
            )
        )

    if not recommendations:
        st.success(
            "No major lifestyle focus area was identified from the "
            "selected wellness inputs."
        )
    else:
        recommendation_columns = st.columns(2)

        for index, (title, description) in enumerate(
            recommendations
        ):
            with recommendation_columns[index % 2]:
                st.markdown(f"### {title}")
                st.write(description)


    # ============================================================
    # Responsible-use notice
    # ============================================================

    st.divider()

    st.warning(
        "Use this result only as an educational model demonstration. "
        "For concerns about mental health, speak with a licensed "
        "professional. Seek urgent support if you feel unsafe."
    )


# ============================================================
# Model evaluation
# ============================================================

if METRICS_PATH.exists():
    st.divider()
    st.markdown("## How well did the model perform?")

    metrics = json.loads(
        METRICS_PATH.read_text(encoding="utf-8")
    )

    columns = st.columns(5)

    metric_items = [
        ("Accuracy", "accuracy"),
        ("Precision", "precision"),
        ("Recall", "recall"),
        ("F1", "f1"),
        ("ROC-AUC", "roc_auc"),
    ]

    for column, (label, key) in zip(
        columns,
        metric_items,
    ):
        with column:
            st.metric(
                label,
                f"{metrics[key]:.3f}",
            )

    st.caption(
        f"Training rows: {metrics['training_rows']:,} · "
        f"Test rows: {metrics['test_rows']:,} · "
        f"Data source: {metrics['data_type']}"
    )

    with st.expander("How to interpret these metrics"):
        st.markdown(
            """
            - **Accuracy:** overall percentage of correct predictions.
            - **Precision:** how often elevated-pattern predictions were correct.
            - **Recall:** how many elevated-pattern examples the model detected.
            - **F1:** balance between precision and recall.
            - **ROC-AUC:** how well the model separates the two classes.

            Because the synthetic dataset is imbalanced, accuracy should not
            be interpreted by itself.
            """
        )


# ============================================================
# Global model feature importance
# ============================================================

if IMPORTANCE_PATH.exists():
    st.divider()
    st.markdown("## What did the model learn overall?")

    st.write(
        "This chart shows which features were most useful across the "
        "entire synthetic training dataset. It is different from the "
        "personal explanation shown after generating a result."
    )

    importance = pd.read_csv(IMPORTANCE_PATH)

    display_names = {
        "depression_score": "Depression score",
        "anxiety_score": "Anxiety score",
        "stress_score": "Stress score",
        "sleep_hours": "Sleep duration",
        "sleep_quality": "Sleep quality",
        "exercise_days": "Exercise frequency",
        "social_support": "Social support",
        "mood_rating": "Mood rating",
        "work_study_hours": "Work or study hours",
        "stressful_events": "Stressful events",
    }

    importance["feature"] = importance["feature"].replace(
        display_names
    )

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
        margin={
            "l": 20,
            "r": 20,
            "t": 20,
            "b": 20,
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.72)",
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displayModeBar": False,
        },
    )


render_footer()