from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey
from backend.db.database import Base
from sqlalchemy.types import DateTime as SQLADateTime
from datetime import datetime,timezone

def naive_now():
    return datetime.now()

class StockData(Base):
    __tablename__="stock_data"
    id=Column(Integer,primary_key=True,index=True)
    timestamp=Column(DateTime,index=True)
    symbol=Column(String,index=True)
    open=Column(Float)
    high=Column(Float)
    low=Column(Float)
    close=Column(Float)
    volume=Column(Integer)

class LivePrice(Base):
    __tablename__="live_price"
    id=Column(Integer,primary_key=True,index=True)
    symbol=Column(String,index=True,nullable=False)
    price=Column(Float,nullable=False)
    currency=Column(String,nullable=False)
    timestamp = Column(
        DateTime,
        default=naive_now,
        index=True
    )

class StockMetadata(Base):
    __tablename__ = "stock_metadata"
    
    symbol       = Column(String, primary_key=True)
    name         = Column(String)
    sector       = Column(String)
    industry     = Column(String)
    market_cap   = Column(Float)
    pe_ratio     = Column(Float)
    currency     = Column(String)
    last_updated = Column(
        DateTime, 
        default=naive_now,
        nullable=False,
        index=True
    )

class TechnicalIndicators(Base):
    __tablename__="technical_indicators"
    id=Column(Integer,primary_key=True,index=True)
    symbol= Column(String, index=True)
    price=Column(Float,nullable=False)
    sma_5=Column(Float)
    sma_10=Column(Float)
    sma_20=Column(Float)
    sma_50=Column(Float)
    sma_100=Column(Float)
    sma_200=Column(Float)
    lag_1=Column(Float)
    lag_2=Column(Float)
    lag_3=Column(Float)
    timestamp = Column(
        DateTime,
        default=naive_now,
        index=True
    )
    

