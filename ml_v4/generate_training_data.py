from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_PATH = Path("data/mindsense_ml_training.csv")
RANDOM_SEED = 42
ROW_COUNT = 6000


def generate_training_data() -> pd.DataFrame:
    """
    Generate synthetic portfolio data for an interactive ML demonstration.

    The target represents elevated depression-risk patterns. This data is
    simulated and must not be described as clinical or real-world data.
    """

    rng = np.random.default_rng(RANDOM_SEED)

    depression_score = rng.integers(0, 43, ROW_COUNT)
    anxiety_score = rng.integers(0, 43, ROW_COUNT)
    stress_score = rng.integers(0, 43, ROW_COUNT)

    sleep_hours = np.clip(rng.normal(7.0, 1.5, ROW_COUNT), 3, 11)
    sleep_quality = rng.integers(1, 6, ROW_COUNT)
    exercise_days = rng.integers(0, 8, ROW_COUNT)
    social_support = rng.integers(1, 6, ROW_COUNT)
    mood_rating = rng.integers(1, 11, ROW_COUNT)
    work_study_hours = np.clip(rng.normal(42, 16, ROW_COUNT), 0, 90)
    stressful_events = rng.integers(0, 6, ROW_COUNT)

    risk_signal = (
        0.16 * depression_score
        + 0.045 * anxiety_score
        + 0.035 * stress_score
        - 0.65 * sleep_hours
        - 0.65 * sleep_quality
        - 0.35 * exercise_days
        - 0.75 * social_support
        - 0.45 * mood_rating
        + 0.025 * work_study_hours
        + 0.75 * stressful_events
        + rng.normal(0, 2.0, ROW_COUNT)
    )

    elevated_risk = (risk_signal > 1.8).astype(int)

    return pd.DataFrame(
        {
            "depression_score": depression_score,
            "anxiety_score": anxiety_score,
            "stress_score": stress_score,
            "sleep_hours": sleep_hours.round(1),
            "sleep_quality": sleep_quality,
            "exercise_days": exercise_days,
            "social_support": social_support,
            "mood_rating": mood_rating,
            "work_study_hours": work_study_hours.round(1),
            "stressful_events": stressful_events,
            "elevated_risk": elevated_risk,
        }
    )


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = generate_training_data()
    data.to_csv(OUTPUT_PATH, index=False)

    print(f"Created synthetic training data: {OUTPUT_PATH}")
    print(f"Rows: {len(data):,}")
    print(data["elevated_risk"].value_counts(normalize=True))


if __name__ == "__main__":
    main()
