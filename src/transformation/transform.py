import os
import pandas as pd
from src.utils.config import load_config

def transform(config_path="config.yaml"):
    cfg=load_config(config_path); raw_dir=cfg["paths"]["raw_dir"]; out_dir=cfg["paths"]["processed_dir"]
    os.makedirs(out_dir,exist_ok=True)
    mm=pd.read_csv(os.path.join(raw_dir,"material_master.csv")); mm=mm.drop_duplicates("material_id"); mm["unit_cost"]=pd.to_numeric(mm["unit_cost"],errors="coerce"); mm=mm.dropna(subset=["unit_cost"]); mm.to_csv(os.path.join(out_dir,"material_master.csv"),index=False)
    sm=pd.read_csv(os.path.join(raw_dir,"supplier_master.csv")).drop_duplicates("supplier_id"); sm.to_csv(os.path.join(out_dir,"supplier_master.csv"),index=False)
    d=pd.read_csv(os.path.join(raw_dir,"material_demand.csv")); d["date"]=pd.to_datetime(d["date"],errors="coerce"); d["demand_qty"]=pd.to_numeric(d["demand_qty"],errors="coerce"); d=d.dropna(subset=["date","material_id"]); d["demand_qty"]=d["demand_qty"].fillna(d["demand_qty"].median()).round().astype(int); d=d[d.demand_qty>=0]; d=d.groupby(["date","material_id","demand_source"],as_index=False)["demand_qty"].sum(); d["date"]=d["date"].dt.strftime("%Y-%m-%d"); d.to_csv(os.path.join(out_dir,"material_demand.csv"),index=False)
    p=pd.read_csv(os.path.join(raw_dir,"purchase_orders.csv")).drop_duplicates("po_id");
    for c in ["ordered_qty","received_qty","rejected_qty","unit_cost"]: p[c]=pd.to_numeric(p[c],errors="coerce")
    for c in ["due_date","receipt_date"]: p[c]=pd.to_datetime(p[c],errors="coerce")
    p=p.dropna(subset=["po_id","material_id","supplier_id","due_date","receipt_date","ordered_qty","received_qty","unit_cost"]); p["rejected_qty"]=p["rejected_qty"].fillna(0).clip(lower=0); p["received_qty"]=p["received_qty"].clip(lower=0); p["ordered_qty"]=p["ordered_qty"].clip(lower=0).round().astype(int); p["received_qty"]=p["received_qty"].round().astype(int); p["rejected_qty"]=p["rejected_qty"].round().astype(int); p.to_csv(os.path.join(out_dir,"purchase_orders.csv"),index=False)
    i=pd.read_csv(os.path.join(raw_dir,"inventory_snapshots.csv")).drop_duplicates(["snapshot_date","material_id"]); i["snapshot_date"]=pd.to_datetime(i["snapshot_date"],errors="coerce"); i=i.dropna(subset=["snapshot_date","material_id"]); i["on_hand_qty"]=pd.to_numeric(i["on_hand_qty"],errors="coerce").fillna(0).clip(lower=0).round().astype(int); i["reserved_qty"]=pd.to_numeric(i["reserved_qty"],errors="coerce").fillna(0).clip(lower=0).round().astype(int); i.to_csv(os.path.join(out_dir,"inventory_snapshots.csv"),index=False)
    return out_dir
