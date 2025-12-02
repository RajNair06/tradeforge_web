import sys,os,time

from fetch_historic import fetch_historical_data
from fetch_live import fetch_live
from prepare_ml_data import prep_data
from datetime import date,timedelta

current_date=date.today()
two_year_ago = current_date - timedelta(days=730)

def unify(symbol,start_date=str(two_year_ago),end_date=str(current_date)):
    fetch_historical_data(symbol,start_date,end_date)
    fetch_live(symbol)
    df=prep_data(symbol)
    
    
    return df




if __name__=="__main__":
    symbol=input("Enter relevant ticker symbol with optional appropriate suffix ( .BO to fetch from Bombay Stock Exchange and .NS to fetch from National Stock Exchange): ")
    fetch_historical_data(symbol,str(two_year_ago),str(current_date))
    fetch_live(symbol)
    prep_data(symbol)
    



    