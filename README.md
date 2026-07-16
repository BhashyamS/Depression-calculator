# MindSense

MindSense is a Streamlit portfolio project built around the DASS-21 self-assessment.

## Versions

- **Version 1:** Classic all-on-one-page questionnaire
- **Version 2:** Enhanced interface with horizontal responses, progress, charts, and recommendations
- **Version 3:** Prototype for recurring check-ins and trend tracking

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```text
MindSense/
├── app.py
├── pages/
├── components/
│   ├── assessment/
│   ├── results/
│   ├── layout/
│   └── ui/
├── core/
├── tests/
└── .streamlit/
```

## Important limitation

MindSense is an educational screening and portfolio project. It is not a diagnosis,
does not assess suicidal thoughts or immediate danger, and does not replace care from
a qualified professional.

## Deploy

Push the repository to GitHub, then deploy through Streamlit Community Cloud with
`app.py` as the main file.

# MindSense Machine Learning Add-On

This add-on forecasts next-week self-reported DASS-21 scores using:
current scores, sleep, exercise, mood, stressful events, social connection, and week number.

The model is a multi-output Random Forest regressor trained on synthetic data.

## Install

# MindSense Kaggle Actigraphy ML

Uses `arashnic/the-depression-dataset`, which contains minute-level actigraphy files for condition and control groups.

## Run

```powershell
python -m pip install -r requirements_kaggle_ml.txt
python -m ml.download_kaggle_data
python -m ml.build_actigraphy_dataset
python -m ml.train_kaggle_model
python -m streamlit run app.py
```

Important: this is a portfolio demonstration, not a clinical model.
