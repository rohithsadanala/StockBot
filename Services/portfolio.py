import requests
import streamlit as st


def get_public_holdings():
    token = st.secrets["PUBLIC_API_KEY"]

    api_url = "https://api.public.com/v2/accounts/me/portfolio"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=15)

        if response.status_code != 200:
            st.error(f"Public API Error {response.status_code}: {response.text}")
            return []

        data = response.json()

        positions = data.get('positions', [])
        holdings = [p['symbol'] for p in positions if 'symbol' in p]

        return holdings

    except Exception as e:
        st.error(f"Connection Error: {e}")
        return []