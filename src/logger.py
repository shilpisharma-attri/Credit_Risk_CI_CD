import logging
import logging.config
import yaml
import os

with open("params.yaml") as f:
    params = yaml.safe_load(f)
log_params = params["logging"]

# Ensure log directory exists
os.makedirs(os.path.dirname(log_params["log_file"]), exist_ok=True)

# Build dictConfig dynamically
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": log_params["log_format"]
        }
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": log_params["log_file"],
            "level": log_params["log_level"],
            "formatter": "default",
        },
    },
    "root": {
        "level": log_params["log_level"],
        "handlers": ["file"],
    },
}

# Add console handler if enabled
if log_params.get("console", True):
    LOGGING_CONFIG["handlers"]["console"] = {
        "class": "logging.StreamHandler",
        "level": log_params["log_level"],
        "formatter": "default",
    }
    LOGGING_CONFIG["root"]["handlers"].append("console")

# Apply config
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("credit_risk_pipeline")



