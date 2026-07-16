import json
import pickle
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor

DATA_PATH = Path("data/weekly_wellness_demo.csv")
MODEL_PATH = Path("models/wellness_forecaster.pkl")
METRICS_PATH = Path("models/model_metrics.json")

FEATURE_COLUMNS = [
    "depression_score", "anxiety_score", "stress_score",
    "sleep_quality", "exercise_days", "mood_rating",
    "stressful_events", "social_connection", "week",
]
TARGET_COLUMNS = [
    "next_depression_score", "next_anxiety_score", "next_stress_score",
]

def train_model():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Dataset missing. Run: python -m ml.generate_demo_data"
        )

    data = pd.read_csv(DATA_PATH)
    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMNS]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=300,
            max_depth=12,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        )
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    metrics = {}
    for i, target in enumerate(TARGET_COLUMNS):
        metrics[target] = {
            "mae": round(mean_absolute_error(y_test.iloc[:, i], predictions[:, i]), 3),
            "r2": round(r2_score(y_test.iloc[:, i], predictions[:, i]), 3),
        }

    bundle = {
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "target_columns": TARGET_COLUMNS,
        "model_name": "Random Forest Multi-Output Regressor",
        "data_type": "Synthetic demonstration data",
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MODEL_PATH.open("wb") as file:
        pickle.dump(bundle, file)

    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics

def main():
    metrics = train_model()
    print(f"Saved model to {MODEL_PATH}")
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
