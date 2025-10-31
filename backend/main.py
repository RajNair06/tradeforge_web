import sys,os
from datetime import datetime
import pytz

from fastapi import FastAPI
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.unify import unify
ist_timezone = pytz.timezone('Asia/Kolkata')
app=FastAPI()

@app.get('/')
def main():
    return {'message':'This is Tradeforge - a live trading simulator'}

@app.get('/latest-features/{symbol}')
def latest_features(symbol):
    unify(symbol)
    current_time_ist = datetime.now(ist_timezone)

    df=pd.read_csv(f'data/ml_{symbol}_data.csv')
    latest=df.iloc[-1].to_dict()
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
                    'lag1': latest.get('lag1', 'N/A'),
                    'lag2': latest.get('lag2', 'N/A'),
                    'lag3': latest.get('lag3', 'N/A')
                },
                'moving_averages': {
                    'sma5': latest.get('sma5', 'N/A'),
                    'sma10': latest.get('sma10', 'N/A'),
                    'sma20': latest.get('sma20', 'N/A'),
                    'sma50': latest.get('sma50', 'N/A'),
                    'sma100': latest.get('sma100', 'N/A'),
                    'sma200': latest.get('sma200', 'N/A')
                }
            }
        },
        'metadata': {
            
            'query_time_IST': current_time_ist.strftime('%Y-%m-%d %H:%M:%S %Z')
        }
    }
    
    return formatted_output

