import requests
import streamlit as st


def get_public_holdings():
    # 1. Pull the Secret from your Streamlit Secrets
    my_secret = st.secrets["PUBLIC_API_KEY"]

    # --- STEP 1: Exchange Secret for Token (POST) ---
    auth_url = "https://api.public.com/userapiauthservice/personal/access-tokens"
    auth_headers = {"Content-Type": "application/json"}
    auth_body = {
        "validityInMinutes": 123,  # Using the value from your example
        "secret": my_secret
    }

    try:
        auth_response = requests.post(auth_url, headers=auth_headers, json=auth_body)

        # If the server returned 200, we proceed to parse the JSON
        if auth_response.status_code == 200:
            token_data = auth_response.json()
            access_token = token_data.get("accessToken")

            if not access_token:
                st.error("Received an empty Access Token. Check your Public.com dashboard.")
                return []

            # --- STEP 2: Fetch Portfolio (GET) ---
            # We use the token from Step 1 in the headers
            portfolio_url = "https://api.public.com/v1/portfolios"
            portfolio_headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }

            port_response = requests.get(portfolio_url, headers=portfolio_headers)

            if port_response.status_code == 200:
                data = port_response.json()
                # Extract symbols from the list of holdings
                return [item['symbol'] for item in data.get('items', [])]
            else:
                st.error(f"Portfolio Fetch Failed: {port_response.status_code}")
                return []
        else:
            st.error(f"Auth Error {auth_response.status_code}: {auth_response.text}")
            return []

    except Exception as e:
        st.error(f"System Error: {e}")
        return []