from database import Base,engine,session
from models import credit_risk
import pandas as pd

Base.metadata.create_all(bind=engine)

df = pd.read_csv('/home/ctp/Training_work/doc/credit_risk/credit_risk_dataset.csv')


try:
    data = df.to_dict(orient='records')

    session.bulk_insert_mappings(credit_risk, data)
    session.commit()
    print("Data inserted successfully")
except Exception as e:
    session.rollback()
    print(f"Error occured: {e}")

