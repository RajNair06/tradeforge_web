from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

DB_FILENAME = "db/trading.db"
ABS_DB_PATH = os.path.abspath(os.path.join(os.getcwd(), DB_FILENAME))
# Use four slashes for absolute file path (sqlite:////absolute/path)
DATABASE_URL = f"sqlite:////{ABS_DB_PATH.lstrip('/')}"  # ensures correct form

print("DATABASE_URL resolved to:", DATABASE_URL) 

engine=create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


