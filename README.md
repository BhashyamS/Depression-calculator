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
