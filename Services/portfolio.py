import requests
import streamlit as st


def get_public_holdings():
    api_key = st.secrets["PUBLIC_API_KEY"]

    # Using the standardized Individual API endpoint
    api_url = "https://api.public.com/v1/portfolios"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)

        # 1. Check if the status is NOT 200
        if response.status_code != 200:
            st.error(f"HTTP Error {response.status_code}: {response.text}")
            return []

        # 2. Check if the body is actually empty
        if not response.text.strip():
            st.error("The server returned a blank page. Your API key might not have permission.")
            return []

        # 3. Only then try to read JSON
        data = response.json()
        return [item['symbol'] for item in data.get('items', [])]

    except Exception as e:
        st.error(f"Critical Connection Error: {e}")
        return []