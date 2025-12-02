import sys,os

from backend.db.database import Base,engine
from backend.db.models import StockData,StockMetadata,LivePrice,TechnicalIndicators

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__=="__main__":
    init_db()