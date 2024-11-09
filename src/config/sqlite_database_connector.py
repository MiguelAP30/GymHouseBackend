from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



database_url = "sqlite:///./GymHouseDB.sqlite"

engine = create_engine(database_url,native_datetime=True,connect_args={ "check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
