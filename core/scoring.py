SUBSCALES = {
    "Depression": [3, 5, 10, 13, 16, 17, 21],
    "Anxiety": [2, 4, 7, 9, 15, 19, 20],
    "Stress": [1, 6, 8, 11, 12, 14, 18],
}

SEVERITY = {
    "Depression": [(9, "Normal"), (13, "Mild"), (20, "Moderate"), (27, "Severe"), (999, "Extremely Severe")],
    "Anxiety": [(7, "Normal"), (9, "Mild"), (14, "Moderate"), (19, "Severe"), (999, "Extremely Severe")],
    "Stress": [(14, "Normal"), (18, "Mild"), (25, "Moderate"), (33, "Severe"), (999, "Extremely Severe")],
}

COLORS = {
    "Normal": "#7BAE8C",
    "Mild": "#A7C98C",
    "Moderate": "#D8B66C",
    "Severe": "#D98C6C",
    "Extremely Severe": "#C96A64",
}

MESSAGES = {
    "Depression": {
        "Normal": "Your responses do not suggest significant depressive symptoms during the past week.",
        "Mild": "You reported a few depressive symptoms. Continue checking in with yourself.",
        "Moderate": "Your responses suggest moderate depressive symptoms. Consider support if they continue.",
        "Severe": "Your responses suggest elevated depressive symptoms. Professional support may be helpful.",
        "Extremely Severe": "Your responses suggest very elevated depressive symptoms. Prompt professional support is recommended.",
    },
    "Anxiety": {
        "Normal": "Your anxiety score falls within the normal range.",
        "Mild": "You reported mild anxiety symptoms during the past week.",
        "Moderate": "Your responses suggest moderate anxiety. Grounding and professional guidance may help.",
        "Severe": "Your responses indicate severe anxiety symptoms. Consider speaking with a healthcare provider.",
        "Extremely Severe": "Your anxiety score is very elevated. Prompt professional support is recommended.",
    },
    "Stress": {
        "Normal": "Your stress score falls within the normal range.",
        "Mild": "You reported mild stress during the past week.",
        "Moderate": "Your stress level is moderately elevated. Rest and reduced overload may help.",
        "Severe": "Your responses suggest a high level of stress. Consider support if this continues.",
        "Extremely Severe": "Your stress score is very high. Prompt professional guidance may be helpful.",
    },
}

def get_severity(scale: str, score: int) -> str:
    for threshold, label in SEVERITY[scale]:
        if score <= threshold:
            return label
    return "Unknown"

def calculate_scores(answers: dict) -> dict:
    results = {}
    for scale, items in SUBSCALES.items():
        raw_score = sum(int(answers[item]) for item in items)
        score = raw_score * 2
        severity = get_severity(scale, score)
        results[scale] = {
            "score": score,
            "severity": severity,
            "color": COLORS[severity],
            "message": MESSAGES[scale][severity],
        }
    return results
