from pathlib import Path
import numpy as np
import pandas as pd
RAW=Path("data/kaggle_depression")
OUT=Path("data/actigraphy_features.csv")

def find_dirs():
    found={}
    for d in RAW.rglob("*"):
        if d.is_dir():
            n=d.name.lower()
            if "condition" in n and "condition" not in found: found["condition"]=d
            if "control" in n and "control" not in found: found["control"]=d
    if set(found)!={"condition","control"}: raise FileNotFoundError("Run python -m ml.download_kaggle_data first")
    return found

def read_file(path):
    df=pd.read_csv(path); cols={c.lower().strip():c for c in df.columns}
    if "activity" not in cols: raise ValueError("Missing activity column")
    df=df.rename(columns={cols["activity"]:"activity"}); df["activity"]=pd.to_numeric(df["activity"],errors="coerce"); df=df.dropna(subset=["activity"])
    if "timestamp" in cols: df["timestamp"]=pd.to_datetime(df[cols["timestamp"]],errors="coerce")
    elif "date" in cols: df["timestamp"]=pd.to_datetime(df[cols["date"]],errors="coerce")
    else: df["timestamp"]=pd.NaT
    return df

def slope(s):
    s=s.dropna().astype(float)
    return float(np.polyfit(np.arange(len(s)),s,1)[0]) if len(s)>1 else 0.0

def extract_features(path,group):
    df=read_file(path); a=df.activity.clip(lower=0)
    f={"participant_id":path.stem,"group":group,"target":1 if group=="condition" else 0,"observation_count":len(a),"activity_mean":a.mean(),"activity_std":a.std(ddof=0),"activity_median":a.median(),"activity_max":a.max(),"activity_q25":a.quantile(.25),"activity_q75":a.quantile(.75),"activity_iqr":a.quantile(.75)-a.quantile(.25),"zero_activity_ratio":(a==0).mean(),"active_ratio":(a>0).mean(),"activity_cv":a.std(ddof=0)/a.mean() if a.mean()>0 else 0.0}
    if df.timestamp.notna().any():
        v=df.dropna(subset=["timestamp"]).copy(); v["hour"]=v.timestamp.dt.hour; v["date_only"]=v.timestamp.dt.date
        day=v.loc[v.hour.between(7,21),"activity"]; night=v.loc[~v.hour.between(7,21),"activity"]; daily=v.groupby("date_only").activity.agg(["mean","std","sum"])
        f.update({"measurement_days":v.date_only.nunique(),"day_activity_mean":day.mean() if len(day) else 0.0,"night_activity_mean":night.mean() if len(night) else 0.0,"day_night_ratio":day.mean()/night.mean() if len(day) and len(night) and night.mean()>0 else 0.0,"daily_mean_std":daily["mean"].std(ddof=0),"daily_total_average":daily["sum"].mean(),"daily_total_std":daily["sum"].std(ddof=0),"daily_activity_trend":slope(daily["mean"])})
    else:
        f.update({"measurement_days":0,"day_activity_mean":0,"night_activity_mean":0,"day_night_ratio":0,"daily_mean_std":0,"daily_total_average":0,"daily_total_std":0,"daily_activity_trend":0})
    return f

def main():
    rows=[]
    for group,d in find_dirs().items():
        for p in sorted(d.rglob("*.csv")):
            try: rows.append(extract_features(p,group))
            except Exception as e: print("Skipping",p,e)
    df=pd.DataFrame(rows); nums=df.select_dtypes("number").columns; df[nums]=df[nums].replace([np.inf,-np.inf],np.nan); df[nums]=df[nums].fillna(df[nums].median())
    OUT.parent.mkdir(parents=True,exist_ok=True); df.to_csv(OUT,index=False); print(df.group.value_counts()); print("Saved",OUT)

if __name__=="__main__": main()
