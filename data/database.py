from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine

url = "postgresql+psycopg2://chat_user:password@localhost/credit_risk_db"

engine = create_engine(url)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()