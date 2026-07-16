import json,pickle
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix
from sklearn.model_selection import train_test_split,StratifiedKFold,cross_val_score
DATA=Path("data/actigraphy_features.csv"); MODEL=Path("models/actigraphy_depression_classifier.pkl"); MET=Path("models/actigraphy_model_metrics.json"); IMP=Path("models/actigraphy_feature_importance.csv")

def main():
    if not DATA.exists(): raise FileNotFoundError("Run download and feature-building scripts first")
    df=pd.read_csv(DATA); features=[c for c in df.columns if c not in {"participant_id","group","target"}]; X=df[features]; y=df.target.astype(int)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=42)
    model=RandomForestClassifier(n_estimators=500,max_depth=8,min_samples_leaf=2,class_weight="balanced",random_state=42,n_jobs=-1); model.fit(Xtr,ytr)
    pred=model.predict(Xte); prob=model.predict_proba(Xte)[:,1]; cv=cross_val_score(model,X,y,cv=StratifiedKFold(5,shuffle=True,random_state=42),scoring="roc_auc")
    metrics={"accuracy":round(accuracy_score(yte,pred),4),"precision":round(precision_score(yte,pred,zero_division=0),4),"recall":round(recall_score(yte,pred,zero_division=0),4),"f1":round(f1_score(yte,pred,zero_division=0),4),"roc_auc":round(roc_auc_score(yte,prob),4),"cv_roc_auc_mean":round(float(cv.mean()),4),"cv_roc_auc_std":round(float(cv.std()),4),"confusion_matrix":confusion_matrix(yte,pred).tolist(),"test_participants":len(yte),"total_participants":len(y)}
    MODEL.parent.mkdir(parents=True,exist_ok=True); pickle.dump({"model":model,"feature_columns":features},MODEL.open("wb")); MET.write_text(json.dumps(metrics,indent=2)); pd.DataFrame({"feature":features,"importance":model.feature_importances_}).sort_values("importance",ascending=False).to_csv(IMP,index=False); print(json.dumps(metrics,indent=2))
if __name__=="__main__": main()
