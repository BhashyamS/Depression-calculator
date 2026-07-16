from ml_v4.generate_training_data import generate_training_data


def test_training_data_shape():
    data = generate_training_data()

    assert len(data) == 6000
    assert "elevated_risk" in data.columns
    assert set(data["elevated_risk"].unique()).issubset({0, 1})
