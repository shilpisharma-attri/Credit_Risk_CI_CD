import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.logger import logger
import os
import yaml

with open("params.yaml") as f:
    params = yaml.safe_load(f)

processed_path = params["data"]["processed_path"]
eda_dir = "data/eda/"

def generate_eda():
    try:
        logger.info("Starting EDA")
        df = pd.read_csv(processed_path)
        os.makedirs(eda_dir, exist_ok=True)

        # Plot target distribution only if present
        if "loan_status" in df.columns:
            plt.figure(figsize=(6,4))
            sns.countplot(x="loan_status", data=df)
            plt.tight_layout()
            plt.savefig(f"{eda_dir}/loan_status_distribution.png")
        else:
            logger.info("loan_status column not found. Skipping target distribution plot.")

        plt.figure(figsize=(10,8))
        corr = df.corr(numeric_only=True)
        sns.heatmap(corr, annot=True, fmt=".2f")
        plt.tight_layout()
        plt.savefig(f"{eda_dir}/correlation_heatmap.png")

        logger.info("EDA completed successfully")
    except Exception as e:
        logger.error(f"EDA failed: {e}")
        raise

if __name__ == "__main__":
    generate_eda()
