import pickle
from functools import lru_cache
from pathlib import Path

import pandas as pd


MODEL_PATH = Path("models/mindsense_risk_model.pkl")


@lru_cache(maxsize=1)
def load_model_bundle() -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"{MODEL_PATH} is missing. Run: python -m ml_v4.train_model"
        )

    with MODEL_PATH.open("rb") as file:
        return pickle.load(file)


def predict_risk(features: dict) -> dict:
    bundle = load_model_bundle()
    feature_columns = bundle["feature_columns"]

    missing = [
        column
        for column in feature_columns
        if column not in features
    ]

    if missing:
        raise ValueError(
            "Missing model inputs: " + ", ".join(missing)
        )

    frame = pd.DataFrame(
        [[features[column] for column in feature_columns]],
        columns=feature_columns,
    )

    probability = float(
        bundle["model"].predict_proba(frame)[0, 1]
    )
    prediction = int(probability >= 0.5)

    return {
        "prediction": prediction,
        "probability": probability,
        "label": (
            "Elevated pattern"
            if prediction == 1
            else "Lower pattern"
        ),
    }
