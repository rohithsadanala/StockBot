from dotenv import load_dotenv
import os

load_dotenv()  # loads your .env file

def get_config(key: str):
    """Get a configuration value from environment variables"""
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Config key '{key}' not found in environment variables")
    return value
