import pickle
from functools import lru_cache
from pathlib import Path

import pandas as pd


MODEL_PATH = Path("models/mindsense_risk_model.pkl")

FEATURE_LABELS = {
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

# Neutral comparison values used only to explain the prediction.
BASELINE_VALUES = {
    "depression_score": 9,
    "anxiety_score": 7,
    "stress_score": 14,
    "sleep_hours": 7.5,
    "sleep_quality": 4,
    "exercise_days": 3,
    "social_support": 4,
    "mood_rating": 7,
    "work_study_hours": 40,
    "stressful_events": 1,
}


@lru_cache(maxsize=1)
def load_model_bundle() -> dict:
    """Load the trained model bundle once per application session."""

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"{MODEL_PATH} is missing. Run: "
            "python -m ml_v4.generate_training_data "
            "and python -m ml_v4.train_model"
        )

    with MODEL_PATH.open("rb") as file:
        return pickle.load(file)


def _build_frame(features: dict, feature_columns: list[str]) -> pd.DataFrame:
    """Convert a feature dictionary into the model's expected format."""

    missing = [
        column
        for column in feature_columns
        if column not in features
    ]

    if missing:
        raise ValueError(
            "Missing model inputs: " + ", ".join(missing)
        )

    return pd.DataFrame(
        [[features[column] for column in feature_columns]],
        columns=feature_columns,
    )


def _predict_probability(
    model,
    features: dict,
    feature_columns: list[str],
) -> float:
    frame = _build_frame(features, feature_columns)
    return float(model.predict_proba(frame)[0, 1])


def explain_prediction(
    features: dict,
    model,
    feature_columns: list[str],
    original_probability: float,
) -> list[dict]:
    """
    Estimate local feature influence using one-feature-at-a-time comparison.

    Each user value is temporarily replaced with a neutral baseline value.
    The resulting probability change estimates how much that feature pushed
    the model's prediction upward or downward for this specific input.

    This is an explanatory approximation, not a causal analysis.
    """

    explanations = []

    for feature in feature_columns:
        comparison_features = features.copy()
        comparison_features[feature] = BASELINE_VALUES[feature]

        baseline_probability = _predict_probability(
            model=model,
            features=comparison_features,
            feature_columns=feature_columns,
        )

        contribution = original_probability - baseline_probability

        explanations.append(
            {
                "feature": feature,
                "label": FEATURE_LABELS[feature],
                "value": features[feature],
                "baseline": BASELINE_VALUES[feature],
                "contribution": contribution,
                "percentage_points": contribution * 100,
                "direction": (
                    "increased"
                    if contribution > 0
                    else "reduced"
                    if contribution < 0
                    else "had little effect on"
                ),
            }
        )

    return sorted(
        explanations,
        key=lambda item: abs(item["contribution"]),
        reverse=True,
    )


def predict_risk(features: dict) -> dict:
    """Generate a probability, label, concern level, and local explanation."""

    bundle = load_model_bundle()

    model = bundle["model"]
    feature_columns = bundle["feature_columns"]

    probability = _predict_probability(
        model=model,
        features=features,
        feature_columns=feature_columns,
    )

    if probability >= 0.70:
        concern_level = "Higher concern pattern"
    elif probability >= 0.40:
        concern_level = "Mixed concern pattern"
    else:
        concern_level = "Lower concern pattern"

    explanations = explain_prediction(
        features=features,
        model=model,
        feature_columns=feature_columns,
        original_probability=probability,
    )

    return {
        "prediction": int(probability >= 0.50),
        "probability": probability,
        "concern_level": concern_level,
        "explanations": explanations,
        "model_name": bundle.get(
            "model_name",
            "Random Forest Classifier",
        ),
        "data_type": bundle.get(
            "data_type",
            "Synthetic demonstration data",
        ),
    }