GENERAL = [
    {"category": "General wellbeing", "title": "Keep a steady routine", "description": "Try to keep sleep, meals, movement, and responsibilities on a predictable schedule."},
    {"category": "General wellbeing", "title": "Stay connected", "description": "Consider checking in with someone you trust when symptoms feel isolating or overwhelming."},
]

CATEGORY = {
    "Depression": {
        "Normal": [{"title": "Protect supportive habits", "description": "Continue routines that support your mood and motivation."}],
        "Mild": [{"title": "Plan one meaningful activity", "description": "Choose one manageable activity that gives enjoyment, connection, or accomplishment."}],
        "Moderate": [{"title": "Break tasks into smaller steps", "description": "Focus on one small step at a time when motivation is low."}],
        "Severe": [{"title": "Reach out for professional support", "description": "Consider contacting a therapist, counselor, doctor, or qualified healthcare professional."}],
        "Extremely Severe": [{"title": "Seek timely professional care", "description": "Very elevated symptoms deserve prompt attention from a licensed professional."}],
    },
    "Anxiety": {
        "Normal": [{"title": "Maintain healthy coping habits", "description": "Continue using routines that help you feel grounded."}],
        "Mild": [{"title": "Try paced breathing", "description": "Use slow breathing with a slightly longer exhale for one or two minutes."}],
        "Moderate": [{"title": "Use a grounding exercise", "description": "Bring attention to what you can see, hear, and feel in the present moment."}],
        "Severe": [{"title": "Seek professional guidance", "description": "A qualified professional can help assess severe anxiety symptoms."}],
        "Extremely Severe": [{"title": "Contact a professional promptly", "description": "Very elevated anxiety symptoms may benefit from timely assessment and support."}],
    },
    "Stress": {
        "Normal": [{"title": "Continue regular recovery time", "description": "Keep making room for rest, movement, and enjoyable activities."}],
        "Mild": [{"title": "Add short recovery breaks", "description": "Take brief pauses to stretch, breathe, or step away from screens."}],
        "Moderate": [{"title": "Reduce unnecessary demands", "description": "Postpone, delegate, or simplify tasks where possible."}],
        "Severe": [{"title": "Address ongoing overload", "description": "Review workload, boundaries, and available support."}],
        "Extremely Severe": [{"title": "Seek support promptly", "description": "Very high stress can affect emotional and physical health."}],
    },
}

ORDER = {"Normal": 0, "Mild": 1, "Moderate": 2, "Severe": 3, "Extremely Severe": 4}

def get_recommendations(results: dict, limit: int = 6) -> list[dict]:
    output = []
    for scale in sorted(results, key=lambda s: ORDER[results[s]["severity"]], reverse=True):
        severity = results[scale]["severity"]
        for item in CATEGORY[scale][severity]:
            output.append({"category": scale, **item})
    output.extend(GENERAL)

    seen, unique = set(), []
    for item in output:
        if item["title"] not in seen:
            seen.add(item["title"])
            unique.append(item)
        if len(unique) >= limit:
            break
    return unique

def requires_professional_support(results: dict) -> bool:
    return any(r["severity"] in {"Severe", "Extremely Severe"} for r in results.values())
