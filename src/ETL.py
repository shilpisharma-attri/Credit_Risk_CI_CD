from src.logger import logger
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


import os
import yaml

# Load config
with open("params.yaml") as f:
    params = yaml.safe_load(f)

RAW_PATH = os.path.abspath(params["data"]["raw_path"])
PROCESSED_PATH = os.path.abspath(params["data"]["processed_path"])

# Ensure directories exist
os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)

# Do not read raw data at import time; read it fresh inside the ETL function

#info about columns
def info_columns(data):
    logger.info(f"DataFrame Info:\n{data.info()}")

# info_columns(data)


#summary statistics
def summary_statistics(data):
    desc=data.describe(include='all')
    logger.info(f"summary statistics:\n{desc}")

# summary_statistics(data)



def check_missing_values(data):
    #checking missing values
    for i in data.columns:
        if data[i].isnull().sum()>0:
            logger.info(f"Column {i} has missing values: missing")

# check_missing_values(data)

def checking_duplicate_value(data):
    #checking duplicate values
    for i in data.columns:
        if data[i].duplicated().sum()>0:
            logger.info(f"Column {i} has duplicate values: {data[i].duplicated().sum()} ")
 
# checking_duplicate_value(data)

def check_outliers(data):
    #checking outliers
    numeric_col=data.select_dtypes(include=[np.float64,np.int64])
    for i in numeric_col:
        q1=data[i].quantile(0.25)
        q3=data[i].quantile(0.75)
        iqr=q3-q1
        lower_bound=q1-1.5*iqr
        upper_bound=q3+1.5*iqr
        outliers=data[(data[i]<lower_bound) | (data[i]>upper_bound)]
        if len(outliers)>0:
            logger.info(f"Column {i} has outliers: {len(outliers)}")

# check_outliers(data)

#value count
def value_count(data):
    for i in data.columns:
        if data[i].dtypes==object:
            vc = data[i].value_counts()
            
            if len(vc)>10:
                logger.info(f"column {i} has more than 10 unique values {vc.head(10)}, skipping value counts.")
            else:
                logger.info(f"column {i} has value counts: {data[i].value_counts()}")

# value_count(data)

#check imbalanced data
def check_imbalanced_data(data):
    for i in data.columns:
        if i=="Exited":
            vc_percentage=data[i].value_counts(normalize=True)
            if (vc_percentage.max()>0.7):
                    logger.info(f"data is imbalanced in column {i} with max percentage {vc_percentage.max()}")
            else:
                logger.info(f"data is balanced in column {i} with max percentage {vc_percentage.max()}")

#handlemissing values

def handle_missing_values(data):
    for i in data.columns:
        if data[i].isnull().sum()>0:
            if data[i].dtypes==object:
                # Avoid chained assignment warnings by assigning the filled series back
                data[i] = data[i].fillna(data[i].mode()[0])
            else:
                data[i] = data[i].fillna(data[i].mean())
    return data


def etl_pre_process(output_path):
    try:
        logger.info("Starting ETL process")
        # Read the latest raw data at runtime
        logger.info(f"Reading raw data from: {RAW_PATH}")
        if not os.path.exists(RAW_PATH):
            raise FileNotFoundError(f"Raw data file not found at {RAW_PATH}. Check params.yaml 'data.raw_path' and working directory.")
        raw_df = pd.read_csv(RAW_PATH)
        data = raw_df.copy()
        data = handle_missing_values(data)
        cat_cols = data.select_dtypes(include=['object']).columns
        for col in cat_cols:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        data.to_csv(output_path, index=False)
        logger.info(f"ETL process completed. Processed data saved to {output_path}")
        return data
    except Exception as e:
        logger.error(f"ETL process failed: {e}")
        raise


processed_csv_path = PROCESSED_PATH


if __name__ == "__main__":
    etl_pre_process(processed_csv_path)
