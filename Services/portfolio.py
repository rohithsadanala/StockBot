import requests
import streamlit as st


def get_public_holdings():
    # 1. Get your Secret from Streamlit Secrets
    my_secret = st.secrets["PUBLIC_API_KEY"]

    # --- STEP 1: POST to get the Access Token ---
    auth_url = "https://api.public.com/userapiauthservice/personal/access-tokens"
    auth_headers = {"Content-Type": "application/json"}
    auth_body = {
        "validityInMinutes": 60,  # Token works for 1 hour
        "secret": my_secret
    }

    try:
        auth_response = requests.post(auth_url, headers=auth_headers, json=auth_body)

        if auth_response.status_code != 200:
            st.error(f"Auth Failed: {auth_response.status_code} - {auth_response.text}")
            return []

        # Extract the temporary token
        token_data = auth_response.json()
        access_token = token_data.get("accessToken")

        # --- STEP 2: GET the Portfolio using the new Token ---
        portfolio_url = "https://api.public.com/v1/portfolios"
        portfolio_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        port_response = requests.get(portfolio_url, headers=portfolio_headers)

        if port_response.status_code == 200:
            data = port_response.json()
            # Loop through items and grab symbols
            return [item['symbol'] for item in data.get('items', [])]
        else:
            st.error(f"Portfolio Error: {port_response.status_code}")
            return []

    except Exception as e:
        st.error(f"System Error: {e}")
        return []