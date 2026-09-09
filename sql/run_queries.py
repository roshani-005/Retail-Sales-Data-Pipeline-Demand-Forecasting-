import os,pandas as pd
from sqlalchemy import create_engine,text
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB=os.path.join(ROOT,"data/warehouse/materials.db")
engine=create_engine(f"sqlite:///{DB}")
sql=open(os.path.join(ROOT,"sql/queries/analysis.sql")).read()
os.makedirs(os.path.join(ROOT,"artifacts/sql_outputs"),exist_ok=True)
for idx,block in enumerate([b.strip() for b in sql.split(';') if b.strip()],1):
    lines=[x for x in block.splitlines() if not x.strip().startswith('--')]
    q='\n'.join(lines).strip()
    if not q: continue
    try:
        df=pd.read_sql(text(q),engine); df.to_csv(os.path.join(ROOT,f"artifacts/sql_outputs/query_{idx:02d}.csv"),index=False); print(f"Q{idx}: {len(df)} rows")
    except Exception as e: print(f"Q{idx} failed: {e}")
