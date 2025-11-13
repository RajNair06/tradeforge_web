import sys,os
from datetime import datetime,timedelta,date
import pytz
import json
import httpx
from redis import Redis
from fastapi import FastAPI,HTTPException,Query,Request
from fastapi.responses import JSONResponse,HTMLResponse

from fastapi.templating import Jinja2Templates
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.unify import unify
from scripts.fetch_historic import fetch_historical_data
from db.models import TechnicalIndicators
from db.database import SessionLocal,engine
ist_timezone = pytz.timezone('Asia/Kolkata')
app=FastAPI()
templates=Jinja2Templates(directory='templates')



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


@app.get('/',response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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





@app.get('/plotting/{symbol}/live', response_class=HTMLResponse)
async def get_live_plotting_data(
    request: Request,
    symbol: str, 
    start_date: str, 
    use_cache: bool = True
):
    """
    Returns an HTML page with Chart.js plot, with caching support
    """
    end_date = date.today()
    metadata_df=pd.read_sql(f"SELECT * FROM stock_metadata WHERE symbol='{symbol}' LIMIT 1 ",engine)

    print(metadata_df.head())
    print(metadata_df.columns)
    name=metadata_df.iloc[0]['name']
    sector=metadata_df.iloc[0]['sector']
    industry=metadata_df.iloc[0]['industry']
    market_cap=metadata_df.iloc[0]['market_cap']
    pe_ratio=metadata_df.iloc[0]['pe_ratio']
    currency=metadata_df.iloc[0]['currency']

    

    
    # Cache keys
    data_cache_key = f'plotting_data_{symbol}_{start_date}_to_{end_date}'
    html_cache_key = f'plotting_html_{symbol}_{start_date}_to_{end_date}'
    
    # Try to get cached HTML first (fastest)
    if use_cache:
        cached_html = app.state.redis.get(html_cache_key)
        if cached_html:
            print("Returning cached HTML")
            return HTMLResponse(content=cached_html.decode('utf-8'))
    
    # Try to get cached data
    filtered_data = None
    if use_cache:
        cached_data = app.state.redis.get(data_cache_key)
        if cached_data:
            print("Using cached data")
            filtered_data = json.loads(cached_data)
    
    # Fetch fresh data if no cache
    if not filtered_data:
        print("Fetching fresh data")
        df = unify(symbol)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        start_dt = pd.to_datetime(start_date)
        
        filtered_df = df[df['timestamp'] >= start_dt]
        
        
        # Convert to list format and cache
        filtered_data = {
            'timestamps': filtered_df['timestamp'].dt.strftime('%Y-%m-%d').tolist(),
            'prices': filtered_df['price'].fillna(0).tolist(),
            'sma20': filtered_df['sma20'].fillna(0).tolist(),
            'sma50': filtered_df['sma50'].fillna(0).tolist(),
            'sma100': filtered_df['sma100'].fillna(0).tolist(),
            'sma200': filtered_df['sma200'].fillna(0).tolist(),
            'lag1': filtered_df['lag1'].fillna(0).tolist(),
            'lag2': filtered_df['lag2'].fillna(0).tolist(),
            'lag3': filtered_df['lag3'].fillna(0).tolist()
        }
        
        # Cache the data for 60 seconds
        if use_cache:
            app.state.redis.setex(data_cache_key, 60, json.dumps(filtered_data))
    
    # Get current data for display
    last_index = len(filtered_data['timestamps']) - 1
    current_data = {
        'price': filtered_data['prices'][last_index] if last_index >= 0 else 0,
        'sma20': filtered_data['sma20'][last_index] if last_index >= 0 else 0,
        'sma50': filtered_data['sma50'][last_index] if last_index >= 0 else 0,
        'sma100': filtered_data['sma100'][last_index] if last_index >= 0 else 0,
        'sma200': filtered_data['sma200'][last_index] if last_index >= 0 else 0,
        'lag1': filtered_data['lag1'][last_index] if last_index >= 0 else 0,
        'lag2': filtered_data['lag2'][last_index] if last_index >= 0 else 0,
        'lag3': filtered_data['lag3'][last_index] if last_index >= 0 else 0,
        'timestamp': filtered_data['timestamps'][last_index] if last_index >= 0 else 'N/A'
    }
    
    # Prepare context for template
    context = {
        "request": request,
        "symbol": symbol,
        "start_date": start_date,
        "end_date": str(end_date),
        "data": filtered_data,
        "current_data": current_data,
        "name":name,
        "sector":sector,
        "industry":industry,
        "market_cap":market_cap,
        "currency":currency,
        "pe_ratio":pe_ratio

    }
    
    # Render template
    html_content = templates.TemplateResponse("create_plot.html", context).body.decode('utf-8')
    
    # Cache the HTML for 60 seconds
    if use_cache:
        app.state.redis.setex(html_cache_key, 60, html_content)
    
    return HTMLResponse(content=html_content)