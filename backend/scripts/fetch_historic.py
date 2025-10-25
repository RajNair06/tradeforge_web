import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import yfinance as yf
import pandas as pd
from db.database import SessionLocal
from db.models import StockData
from datetime import datetime

def fetch_historical_data(symbol: str, start_date: str, end_date: str):
    try:
        # Fetch data using yfinance
        df = yf.download(symbol, start=start_date, end=end_date, interval="1d")

        
        format_string="%Y-%m-%d"
        start_date=datetime.strptime(start_date,format_string)
        end_date=datetime.strptime(end_date,format_string)
        print((end_date-start_date).days)
    
    
        
        
        df=df.reset_index()
        df.columns = [col[0] for col in df.columns.values]
        
        print(df.columns)

        df['Symbol']=symbol
        df.to_csv(f'data/{symbol}_{(end_date-start_date).days}_days.csv')
        
        
    

        
        
        with SessionLocal() as db:
            try:
                for _, row in df.iterrows():
                    stock_data = StockData(
                        timestamp=row['Date'],
                        symbol=symbol,
                        open=row['Open'],
                        high=row['High'],
                        low=row['Low'],
                        close=row['Close'],
                        volume=int(row['Volume'])
                    )
                    db.add(stock_data)
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error saving to database: {e}")
        
        return df

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


if __name__ == "__main__":
    symbol ='RELIANCE.BO' #input("Enter ticker symbol(add suffix .BO to fetch from BSE): ")
    start_date ='2024-10-19' #input("Enter start date in the format YYYY-MM-DD: ")
    end_date ='2025-10-19' # input("Enter end date in the format YYYY-MM-DD: ")
    data = fetch_historical_data(symbol, start_date, end_date)
    if data is not None:
        print(data.head())
        