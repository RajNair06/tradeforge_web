import sys,os,time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import yfinance as yf
from db.database import SessionLocal
from db.models import LivePrice,StockMetadata
from datetime import datetime,timezone

POLL_INTERVAL=30

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
        

def main():
    SYMBOL=input("Enter ticker symbol(Add relevant suffixes to specify exchance ex: add .BO for BSE and .NS for NSE): ")
    print(f"Starting live polling for {SYMBOL} every {POLL_INTERVAL}s...")
    info=get_ticker_info(SYMBOL)

    with SessionLocal() as db:
        update_metadata(db,SYMBOL,info)
        while True:
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
            
            time.sleep(POLL_INTERVAL)


if __name__=="__main__":
    main()
    
