import sys,os,time

import yfinance as yf
from db.database import SessionLocal
from db.models import LivePrice,StockMetadata
from datetime import datetime,timedelta

# POLL_INTERVAL=30
# RUN_FOR_MINUTES=2
# END_TIME=datetime.now()+timedelta(minutes=RUN_FOR_MINUTES)

def get_ticker_info(symbol:str):
    ticker=yf.Ticker(symbol)
    return ticker.info


def update_metadata(db, symbol: str, info: dict):
    meta = db.query(StockMetadata).filter(StockMetadata.symbol == symbol).first()
    
    
    now = datetime.now()
    
    if not meta or (now - meta.last_updated).days >= 1:
        if not meta:
            meta = StockMetadata(symbol=symbol)
            db.add(meta)  

        
        meta.name=info.get("longName")
        meta.sector =info.get("sector")
        meta.industry   = info.get("industry")
        meta.market_cap = info.get("marketCap")
        meta.pe_ratio   = info.get("trailingPE")
        meta.currency   = info.get("currency", "UNKNOWN")
        meta.last_updated = now

        db.commit()
        print(f"Metadata updated for {symbol} | {meta.currency}")
        

def fetch_live(symbol):
    SYMBOL=symbol
    # print(f"Starting live polling for {SYMBOL} every {POLL_INTERVAL}s...")
    print(f'Fetching live data for {SYMBOL}...')
    info=get_ticker_info(SYMBOL)

    with SessionLocal() as db:
        update_metadata(db,SYMBOL,info)
        # while datetime.now()<END_TIME:
        try:
                ticker=get_ticker_info(SYMBOL)
                price=ticker.get("regularMarketPrice")
                currency=ticker.get("currency","UNKNOWN")
                if price:
                    db.add(LivePrice(symbol=SYMBOL,price=price,currency=currency))
                    
                    db.commit()
                    print(f"{time.strftime('%H:%M:%S')} | {SYMBOL} = {price:.2f}")
                else:
                        print(f"No price data at {time.strftime('%H:%M:%S')}")
                    
        except Exception as e:
                print(f"Error: {e}")
            
        # time.sleep(POLL_INTERVAL)


if __name__=="__main__":
    fetch_live()
    
