import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

df=pd.read_csv('data/ml_TCS.BO_data.csv')

df['next_day_price']=df['price'].shift(-1)

print(df[:-1])