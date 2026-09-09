import os,sys,json
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.transformation.transform import transform
from src.loading.load import load
from src.ml.forecast_model import train_and_forecast
from src.utils.config import load_config

def run():
 cfg=load_config(); transform(); load(); metrics=train_and_forecast(); print("Pipeline complete",metrics); return metrics
if __name__=="__main__": run()
