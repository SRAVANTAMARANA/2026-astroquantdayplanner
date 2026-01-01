import os

"""
config.py
---------
Configuration loader for AstroQuant Day Planner
Loads user config from YAML file, with docstrings and error handling.
"""

import yaml
import logging

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY", "")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")

def load_config(path='user_config.yaml'):
    """
    Load user configuration from a YAML file.

    Args:
        path (str): Path to the YAML config file.

    Returns:
        dict: Configuration dictionary, or empty dict if error.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Error loading config from {path}: {e}")
        return {}

if __name__ == "__main__":
    print(load_config())
