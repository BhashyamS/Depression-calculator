import pickle
from functools import lru_cache
from pathlib import Path
import pandas as pd
from ml.build_actigraphy_dataset import extract_features
MODEL=Path("models/actigraphy_depression_classifier.pkl")
@lru_cache(maxsize=1)
def load_bundle():
    if not MODEL.exists(): raise FileNotFoundError("Train the model first")
    return pickle.load(MODEL.open("rb"))
def predict_uploaded(uploaded):
    temp=Path("data/_uploaded_activity.csv"); temp.parent.mkdir(parents=True,exist_ok=True); temp.write_bytes(uploaded.getvalue())
    try: f=extract_features(temp,"unknown")
    finally: temp.unlink(missing_ok=True)
    b=load_bundle(); frame=pd.DataFrame([{c:f.get(c,0.0) for c in b["feature_columns"]}]); p=float(b["model"].predict_proba(frame)[0,1]); return {"probability":p,"label":"Condition-like activity pattern" if p>=.5 else "Control-like activity pattern"}
