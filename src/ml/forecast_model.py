import os, json, joblib, numpy as np, pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
from src.utils.config import load_config

FEATURES=["dow","month","lag_1","lag_7","rolling_7"]

def make_features(df):
    d=df.copy(); d["date"]=pd.to_datetime(d["date"]); d=d.groupby("date",as_index=False)["demand_qty"].sum().sort_values("date"); d["dow"]=d.date.dt.dayofweek; d["month"]=d.date.dt.month; d["lag_1"]=d.demand_qty.shift(1); d["lag_7"]=d.demand_qty.shift(7); d["rolling_7"]=d.demand_qty.shift(1).rolling(7).mean(); return d.dropna().reset_index(drop=True)

def model(): return XGBRegressor(n_estimators=250,max_depth=4,learning_rate=.05,subsample=.9,colsample_bytree=.9,objective="reg:squarederror",random_state=42,n_jobs=2)

def train_and_forecast(config_path="config.yaml"):
    cfg=load_config(config_path); engine=create_engine(f"sqlite:///{cfg['database']['path']}"); demand=pd.read_sql("SELECT date,demand_qty FROM material_demand",engine); d=make_features(demand); split=int(len(d)*.8); m=model(); m.fit(d.iloc[:split][FEATURES],d.iloc[:split].demand_qty); pred=m.predict(d.iloc[split:][FEATURES]); metrics={"mae":float(mean_absolute_error(d.iloc[split:].demand_qty,pred)),"rmse":float(np.sqrt(mean_squared_error(d.iloc[split:].demand_qty,pred))),"horizon_days":int(cfg['forecast']['horizon_days'])}
    final=model(); final.fit(d[FEATURES],d.demand_qty); hist=d[["date","demand_qty"]].copy(); rows=[]
    for _ in range(metrics["horizon_days"]):
        nd=hist.date.max()+pd.Timedelta(days=1); r=pd.DataFrame([{"dow":nd.dayofweek,"month":nd.month,"lag_1":hist.demand_qty.iloc[-1],"lag_7":hist.demand_qty.iloc[-7],"rolling_7":hist.demand_qty.tail(7).mean()}]); p=max(0,float(final.predict(r[FEATURES])[0])); rows.append([nd,p]); hist=pd.concat([hist,pd.DataFrame([[nd,p]],columns=["date","demand_qty"])],ignore_index=True)
    os.makedirs("artifacts",exist_ok=True); pd.DataFrame(rows,columns=["date","forecast_demand_qty"]).to_csv("artifacts/demand_forecast.csv",index=False); joblib.dump(final,"artifacts/demand_forecast_xgb.joblib"); json.dump(metrics,open("artifacts/forecast_metrics.json","w"),indent=2); return metrics
