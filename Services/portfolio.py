import requests
import streamlit as st


def get_public_holdings():
    api_key = st.secrets["PUBLIC_API_KEY"]

    api_url = "https://api.public.com/v1/portfolios"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            st.error(f"Public API Error: {response.status_code} - {response.text}")
            return []

        data = response.json()
        return [item['symbol'] for item in data.get('items', [])]

    except Exception as e:
        st.error(f"Connection Error: {e}")
        return []