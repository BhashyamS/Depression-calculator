import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from components.layout.footer import render_footer
from components.ui.styles import load_styles
from ml.actigraphy_predictor import MODEL,predict_uploaded
MET=Path("models/actigraphy_model_metrics.json"); IMP=Path("models/actigraphy_feature_importance.csv")
load_styles(); st.title("Actigraphy Machine Learning"); st.caption("Real Kaggle actigraphy data + Random Forest")
st.warning("This model compares activity patterns with the dataset's condition and control groups. It does not diagnose depression and is separate from DASS-21 scoring.")
if not MODEL.exists(): st.error("Train the model first: `python -m ml.download_kaggle_data`, `python -m ml.build_actigraphy_dataset`, `python -m ml.train_kaggle_model`"); st.stop()
uploaded=st.file_uploader("Upload an actigraphy CSV",type=["csv"],help="Requires an activity column; timestamp is recommended.")
if uploaded is not None:
    preview=pd.read_csv(uploaded); uploaded.seek(0); st.dataframe(preview.head(20),use_container_width=True,hide_index=True)
    if "activity" not in {c.lower().strip() for c in preview.columns}: st.error("CSV needs an activity column")
    elif st.button("Analyze Activity Pattern",type="primary",use_container_width=True):
        r=predict_uploaded(uploaded); st.metric("Condition-group similarity",f"{r['probability']*100:.1f}%"); st.subheader(r["label"]); st.progress(r["probability"]); st.caption("This is similarity to dataset groups, not probability of depression.")
if MET.exists():
    st.divider(); st.subheader("Model Evaluation"); m=json.loads(MET.read_text()); cols=st.columns(5)
    for col,(k,label) in zip(cols,[("accuracy","Accuracy"),("precision","Precision"),("recall","Recall"),("f1","F1"),("roc_auc","ROC-AUC")]):
        with col: st.metric(label,f"{m[k]:.3f}")
if IMP.exists():
    st.divider(); st.subheader("Feature Importance"); df=pd.read_csv(IMP).head(12).sort_values("importance"); fig=px.bar(df,x="importance",y="feature",orientation="h"); fig.update_layout(height=470,margin={"l":20,"r":20,"t":20,"b":20},paper_bgcolor="rgba(0,0,0,0)"); st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
render_footer()
