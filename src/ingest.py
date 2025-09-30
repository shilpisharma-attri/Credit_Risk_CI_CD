import pandas as pd
from data.database import engine
from src.logger import logger
import os
import yaml


def run_ingestion():
    try:
        # Load configuration
        with open("params.yaml") as f:
            params = yaml.safe_load(f)

        raw_data_path = os.path.abspath(params["data"]["raw_path"])
        os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)

        logger.info("Starting data ingestion from database")

        # Stream from DB in chunks to limit memory
        chunk_iter = pd.read_sql("select * from credits_risk", con=engine, chunksize=500)
        chunks = []
        for chunk in chunk_iter:
            chunks.append(chunk)

        if not chunks:
            raise RuntimeError("No data returned from database query 'credits_risk'")

        df = pd.concat(chunks, ignore_index=True)

        # Save to CSV
        logger.info(f"Writing raw data to: {raw_data_path}")
        df.to_csv(raw_data_path, index=False)
        logger.info(f"Data is loaded and saved to {raw_data_path}")

    except Exception as e:
        logger.error(f"Data ingestion failed: {e}")
        raise


if __name__ == "__main__":
    run_ingestion()

