import pandas as pd
import sys,os
from datetime import datetime

from db.models import StockData,LivePrice,TechnicalIndicators
from db.database import SessionLocal,engine
symbol='RELIANCE.BO'

def prep_data(symbol):
    with SessionLocal() as db:
        hist_df=pd.read_sql(f"SELECT symbol,close AS price,timestamp FROM stock_data WHERE symbol='{symbol}'",engine)
        
        live_df=pd.read_sql(f"SELECT symbol,price,timestamp FROM live_price WHERE symbol='{symbol}' ORDER BY timestamp DESC LIMIT 1",engine)
        df = pd.concat([hist_df, live_df], ignore_index=True)
        df = df.sort_values("timestamp").drop_duplicates(subset=["timestamp"]).reset_index()
        
        lags=[1,2,3]
        for lag in lags:
            df[f'lag{lag}']=df['price'].shift(lag)
        df=df.dropna().reset_index()
        df=df.drop(['index','level_0'],axis=1)
        df['sma5']=df['price'].rolling(5).mean()
        df['sma10']=df['price'].rolling(10).mean()
        df['sma20']=df['price'].rolling(20).mean()
        df['sma50'] = df['price'].rolling(50).mean()
        df['sma100'] = df['price'].rolling(100).mean()
        df['sma200'] = df['price'].rolling(200).mean()
        df=df.dropna()
        
        
        # OUTPUT_CSV=f"data/ml_{symbol}_data.csv"
        # df.to_csv(OUTPUT_CSV)
        for _,row in df.iterrows():
            technical_indicators = TechnicalIndicators(
                        timestamp=datetime.strptime(row['timestamp'],"%Y-%m-%d %H:%M:%S.%f"),
                        symbol=symbol,
                        price=row['price'],
                        sma_5=row['sma5'],
                        sma_10=row['sma10'],
                        sma_20=row['sma20'],
                        sma_50=row['sma50'],
                        sma_100=row['sma100'],
                        sma_200=row['sma200'],
                        lag_1=row['lag1'],
                        lag_2=row['lag2'],
                        lag_3=row['lag3']
                        )
                    
            db.add(technical_indicators)
            db.commit()
        return df

            


