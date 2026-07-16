def detect_large_changes(current_scores, predicted_scores, threshold=8.0):
    alerts = []
    for scale in ["Depression", "Anxiety", "Stress"]:
        change = predicted_scores[scale] - current_scores[scale]
        if abs(change) >= threshold:
            direction = "increase" if change > 0 else "decrease"
            alerts.append(
                f"{scale} has a predicted {direction} of {abs(change):.1f} points."
            )
    return alerts
