from database import Base, engine
from sqlalchemy import Column, Integer, String, Float, BigInteger


class credit_risk(Base):
    __tablename__ = 'credits_risk'
    ID = Column(Float,primary_key=True, autoincrement=True)
    person_age = Column(Float)
    person_income = Column(Float)
    person_home_ownership = Column(String)
    person_emp_length = Column(Float)
    loan_intent = Column(String)
    loan_grade = Column(String)
    loan_amnt = Column(Float)
    loan_int_rate = Column(Float)
    loan_status = Column(String)
    loan_percent_income = Column(Float)
    cb_person_default_on_file = Column(String)
    cb_person_cred_hist_length = Column(Float)
    
  