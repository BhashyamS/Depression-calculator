import json
import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


DATA_PATH = Path("data/mindsense_ml_training.csv")
MODEL_PATH = Path("models/mindsense_risk_model.pkl")
METRICS_PATH = Path("models/mindsense_risk_metrics.json")
IMPORTANCE_PATH = Path("models/mindsense_risk_feature_importance.csv")

FEATURE_COLUMNS = [
    "depression_score",
    "anxiety_score",
    "stress_score",
    "sleep_hours",
    "sleep_quality",
    "exercise_days",
    "social_support",
    "mood_rating",
    "work_study_hours",
    "stressful_events",
]


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"{DATA_PATH} does not exist. Run: "
            "python -m ml_v4.generate_training_data"
        )

    data = pd.read_csv(DATA_PATH)

    X = data[FEATURE_COLUMNS]
    y = data["elevated_risk"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=400,
        max_depth=10,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, predictions), 4),
        "precision": round(
            precision_score(y_test, predictions, zero_division=0),
            4,
        ),
        "recall": round(
            recall_score(y_test, predictions, zero_division=0),
            4,
        ),
        "f1": round(f1_score(y_test, predictions), 4),
        "roc_auc": round(roc_auc_score(y_test, probabilities), 4),
        "confusion_matrix": confusion_matrix(
            y_test,
            predictions,
        ).tolist(),
        "classification_report": classification_report(
            y_test,
            predictions,
            target_names=["Lower pattern", "Elevated pattern"],
            output_dict=True,
            zero_division=0,
        ),
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "data_type": "Synthetic portfolio demonstration data",
    }

    bundle = {
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "model_name": "Random Forest Classifier",
        "target_name": "Elevated depression-risk pattern",
        "data_type": "Synthetic portfolio demonstration data",
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    with MODEL_PATH.open("wb") as file:
        pickle.dump(bundle, file)

    METRICS_PATH.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    importance = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    importance.to_csv(IMPORTANCE_PATH, index=False)

    print(f"Saved model: {MODEL_PATH}")
    print(f"Saved metrics: {METRICS_PATH}")
    print(f"Saved feature importance: {IMPORTANCE_PATH}")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
