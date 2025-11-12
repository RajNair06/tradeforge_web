import sys,os
from datetime import datetime,timedelta,date
import pytz
import json
import httpx
from redis import Redis
from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import JSONResponse
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

@app.on_event("startup")
async def startup_event():
    app.state.redis=Redis(host='localhost',port=6379)

@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()


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
async def historical_data(symbol,start_date,end_date,offset=0,limit=50):
    value=app.state.redis.get(f'historical_data_{symbol}_{start_date}_to_{end_date}')

    if value:
        
        cached_data = json.loads(value)
        paginated_data = paginate_data(cached_data, offset, limit)
        return paginated_data
    else:
        
        df=fetch_historical_data(symbol=symbol,start_date=start_date,end_date=end_date)
        df['Date'] = df['Date'].astype(str)
        json_string=df.to_json(orient='records')
        full_data=json.loads(json_string)
        app.state.redis.set(f'historical_data_{symbol}_{start_date}_to_{end_date}',json.dumps(full_data))
        paginated_data = paginate_data(full_data, offset, limit)
        return paginated_data



@app.get('/plotting/{symbol}/live')
async def get_live_plotting_data(symbol: str, start_date: str, offset: int = 0, limit: int = 50):
    """
    Get plotting data for a symbol with caching and pagination
    Returns the exact DataFrame structure from unify()
    """
    end_date=date.today()
    cache_key = f'plotting_data_{symbol}_{start_date}_to_{end_date}'
    value = app.state.redis.get(cache_key)

    if value:
        cached_data = json.loads(value)
        paginated_data = paginate_data(cached_data, offset, limit)
        return paginated_data
    else:
        # Get data from unify (which only takes symbol)
        df = unify(symbol)
        
        # Convert timestamp to datetime for filtering
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Convert query params to datetime
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        # Filter DataFrame by date range
        filtered_df = df[(df['timestamp'] >= start_dt) & (df['timestamp'] <= end_dt)]
        
        # Convert timestamp back to string for JSON serialization
        filtered_df['timestamp'] = filtered_df['timestamp'].astype(str)
        
        
        json_string = filtered_df.to_json(orient='records')
        full_data = json.loads(json_string)
        app.state.redis.setex(cache_key, 60, json.dumps(full_data))
        paginated_data = paginate_data(full_data, offset, limit)
        
        return paginated_data