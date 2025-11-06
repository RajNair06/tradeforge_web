import sys,os
from datetime import datetime
import pytz

from fastapi import FastAPI
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.unify import unify
from db.models import TechnicalIndicators
from db.database import SessionLocal,engine
ist_timezone = pytz.timezone('Asia/Kolkata')
app=FastAPI()

@app.get('/')
def main():
    return {'message':'This is Tradeforge - a live trading simulator'}

@app.get('/latest-features/{symbol}')
def latest_features(symbol):
    unify(symbol)
    current_time_ist = datetime.now(ist_timezone)

    # df=pd.read_csv(f'data/ml_{symbol}_data.csv')
    df=pd.read_sql(f"SELECT * FROM technical_indicators WHERE symbol='{symbol}' ORDER BY timestamp DESC LIMIT 1",engine)
    latest=df.iloc[-1].to_dict()
    print(latest)

    formatted_output = {
        'symbol': symbol,
        'latest_features': {
            'basic_info': {
                'symbol': latest.get('symbol', 'N/A'),
                'price': latest.get('price', 'N/A'),
                'timestamp': latest.get('timestamp', 'N/A')
            },
            'technical_indicators': {
                'lag_prices': {
                    'lag1': latest.get('lag_1', 'N/A'),
                    'lag2': latest.get('lag_2', 'N/A'),
                    'lag3': latest.get('lag_3', 'N/A')
                },
                'moving_averages': {
                    'sma5': latest.get('sma_5', 'N/A'),
                    'sma10': latest.get('sma_10', 'N/A'),
                    'sma20': latest.get('sma_20', 'N/A'),
                    'sma50': latest.get('sma_50', 'N/A'),
                    'sma100': latest.get('sma_100', 'N/A'),
                    'sma200': latest.get('sma_200', 'N/A')
                }
            }
        },
        'metadata': {
            
            'query_time_IST': current_time_ist.strftime('%Y-%m-%d %H:%M:%S %Z')
        }
    }
    
    return formatted_output

