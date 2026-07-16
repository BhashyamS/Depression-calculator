from pathlib import Path
import numpy as np
import pandas as pd

OUTPUT_PATH = Path("data/weekly_wellness_demo.csv")
RANDOM_SEED = 42
N_USERS = 300
N_WEEKS = 8

def clamp(value, minimum=0, maximum=42):
    return float(np.clip(value, minimum, maximum))

def generate_demo_data():
    rng = np.random.default_rng(RANDOM_SEED)
    rows = []

    for user_id in range(1, N_USERS + 1):
        depression = rng.uniform(2, 28)
        anxiety = rng.uniform(2, 24)
        stress = rng.uniform(4, 30)

        for week in range(1, N_WEEKS + 1):
            sleep_quality = int(rng.integers(1, 6))
            exercise_days = int(rng.integers(0, 8))
            mood_rating = int(rng.integers(1, 11))
            stressful_events = int(rng.integers(0, 6))
            social_connection = int(rng.integers(1, 6))

            next_depression = clamp(
                depression + 1.5 * stressful_events - 1.6 * sleep_quality
                - 0.8 * exercise_days - 0.9 * social_connection
                - 0.7 * mood_rating + 12 + rng.normal(0, 2.8)
            )
            next_anxiety = clamp(
                anxiety + 1.7 * stressful_events - 1.3 * sleep_quality
                - 0.5 * exercise_days - 0.5 * social_connection
                - 0.4 * mood_rating + 8 + rng.normal(0, 2.8)
            )
            next_stress = clamp(
                stress + 2.0 * stressful_events - 1.4 * sleep_quality
                - 0.6 * exercise_days - 0.7 * social_connection
                - 0.4 * mood_rating + 9 + rng.normal(0, 3.0)
            )

            rows.append({
                "user_id": user_id,
                "week": week,
                "depression_score": round(depression, 2),
                "anxiety_score": round(anxiety, 2),
                "stress_score": round(stress, 2),
                "sleep_quality": sleep_quality,
                "exercise_days": exercise_days,
                "mood_rating": mood_rating,
                "stressful_events": stressful_events,
                "social_connection": social_connection,
                "next_depression_score": round(next_depression, 2),
                "next_anxiety_score": round(next_anxiety, 2),
                "next_stress_score": round(next_stress, 2),
            })

            depression, anxiety, stress = next_depression, next_anxiety, next_stress

    return pd.DataFrame(rows)

def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = generate_demo_data()
    data.to_csv(OUTPUT_PATH, index=False)
    print(f"Created {OUTPUT_PATH} with {len(data):,} rows")

if __name__ == "__main__":
    main()
