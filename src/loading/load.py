import os, pandas as pd
from sqlalchemy import create_engine, text
from src.utils.config import load_config

def load(config_path="config.yaml"):
    cfg=load_config(config_path); db=cfg["database"]["path"]; os.makedirs(os.path.dirname(db),exist_ok=True); engine=create_engine(f"sqlite:///{db}")
    root=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    with open(os.path.join(root,"sql","schema.sql")) as f: schema=f.read()
    with engine.begin() as c:
        for stmt in schema.split(';'):
            if stmt.strip(): c.execute(text(stmt))
    files=["material_master","supplier_master","material_demand","purchase_orders","inventory_snapshots"]
    for name in files:
        df=pd.read_csv(os.path.join(cfg["paths"]["processed_dir"],name+".csv")); df.to_sql(name,engine,if_exists="replace",index=False)
    return db
