import sys,os
from datetime import datetime
import pytz
import json
from fastapi import FastAPI
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.unify import unify
from scripts.fetch_historic import fetch_historical_data
from db.models import TechnicalIndicators
from db.database import SessionLocal,engine
ist_timezone = pytz.timezone('Asia/Kolkata')
app=FastAPI()

def paginate_data(data,offset,limit):
    start=offset
    end=offset+limit
    return data[start:end]

@app.get('/')
def main():
    return {'message':'This is Tradeforge - a live trading simulator'}

@app.get('/latest-features/{symbol}')
async def latest_features(symbol):
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

@app.get('/historical-data/{symbol}')
def historical_data(symbol,start_date,end_date,offset=0,limit=50):
    df=fetch_historical_data(symbol=symbol,start_date=start_date,end_date=end_date)
    df['Date'] = df['Date'].astype(str)
    json_string=df.to_json(orient='records')
    json_string=json.loads(json_string)
    paginated_data=paginate_data(json_string,offset,limit)
    return paginated_data



