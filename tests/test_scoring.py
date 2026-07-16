from core.scoring import calculate_scores, get_severity

def test_zero_scores():
    answers = {i:0 for i in range(1,22)}
    results = calculate_scores(answers)
    assert results["Depression"]["score"] == 0
    assert results["Anxiety"]["score"] == 0
    assert results["Stress"]["score"] == 0

def test_max_scores():
    answers = {i:3 for i in range(1,22)}
    results = calculate_scores(answers)
    assert all(results[scale]["score"] == 42 for scale in results)

def test_boundaries():
    assert get_severity("Depression", 9) == "Normal"
    assert get_severity("Depression", 10) == "Mild"
    assert get_severity("Anxiety", 20) == "Extremely Severe"
