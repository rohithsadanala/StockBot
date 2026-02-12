import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_config(key_name):
    # 1. First, check if we are on Streamlit Cloud
    if key_name in st.secrets:
        return st.secrets[key_name]

    # 2. Otherwise, check local .env
    return os.getenv(key_name)