import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import lightgbm as lgb
import mlflow
import mlflow.sklearn
from src.logger import logger
import yaml
import os

# Load params
with open("params.yaml") as f:
    params = yaml.safe_load(f)

processed_path = params["data"]["processed_path"]
test_size = params["model"]["test_size"]
random_state = params["model"]["random_state"]
hyperparams = params["hyperparameters"]

# Ensure MLflow logs to project root
mlflow.set_tracking_uri(os.path.abspath("mlruns"))
mlflow.set_experiment("Credit_Risk_Models")  # Optional: groups runs under one experiment

def train_models():
    try:
        logger.info("Starting training with hyperparameter tuning")
        df = pd.read_csv(processed_path)

        # Change 'loan_status' to your target column
        if "loan_status" not in df.columns:
            raise ValueError(
                "Processed dataset does not contain a 'loan_status' column."
            )

        X = df.drop("loan_status", axis=1)
        y = df["loan_status"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        models = {
            "RandomForest": (RandomForestClassifier(random_state=random_state), hyperparams["random_forest"]),
            "XGBoost": (xgb.XGBClassifier(random_state=random_state, use_label_encoder=False, eval_metric='logloss'),
                        hyperparams["xgboost"]),
            "LightGBM": (lgb.LGBMClassifier(random_state=random_state), hyperparams["lightgbm"])
        }

        for name, (model, params_grid) in models.items():
            logger.info(f"GridSearch for {name}")
            gs = GridSearchCV(model, params_grid, cv=3, scoring='roc_auc', n_jobs=-1)
            gs.fit(X_train, y_train)

            # Predict probabilities safely
            if hasattr(gs.best_estimator_, "predict_proba"):
                y_pred = gs.best_estimator_.predict_proba(X_test)[:,1]
            else:  # fallback for models without predict_proba
                y_pred = gs.best_estimator_.predict(X_test)

            roc_auc = roc_auc_score(y_test, y_pred)

            # Start MLflow run
            with mlflow.start_run(run_name=f"{name}_HPO", nested=True):
                mlflow.sklearn.log_model(gs.best_estimator_, f"{name}_model")
                mlflow.log_params(gs.best_params_)
                mlflow.log_metrics({"roc_auc": roc_auc})
                logger.info(f"{name} trained. ROC-AUC: {roc_auc}")

        logger.info("All models trained and logged successfully.")

    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise

if __name__ == "__main__":
    train_models()
