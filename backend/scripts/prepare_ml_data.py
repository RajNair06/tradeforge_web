import pandas as pd
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.models import StockData,LivePrice
from db.database import SessionLocal,engine
symbol='RELIANCE.BO'
OUTPUT_CSV=f"data/ml_{symbol}_data.csv"

with SessionLocal() as db:
    hist_df=pd.read_sql(f"SELECT symbol,close AS price,timestamp FROM stock_data WHERE symbol='{symbol}'",engine)
    
    live_df=pd.read_sql(f"SELECT symbol,price,timestamp FROM live_price WHERE symbol='{symbol}'",engine)
    df = pd.concat([hist_df, live_df], ignore_index=True)
    df = df.sort_values("timestamp").drop_duplicates(subset=["timestamp"]).reset_index()
    
    lags=[1,2,3]
    for lag in lags:
        df[f'lag{lag}']=df['price'].shift(lag)
    df=df.dropna().reset_index()
    df=df.drop(['index','level_0'],axis=1)
    df.to_csv(OUTPUT_CSV)
