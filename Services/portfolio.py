import requests
import streamlit as st


def get_detailed_portfolio():
    secret_key = st.secrets["PUBLIC_API_KEY"]

    # 1. Get Access Token (Standard POST flow we verified)
    auth_url = "https://api.public.com/userapiauthservice/personal/access-tokens"
    auth_res = requests.post(auth_url, json={"validityInMinutes": 60, "secret": secret_key})
    token = auth_res.json().get("accessToken")

    # 2. Get Portfolio V2 (Using your specific account ID from the JSON)
    # Note: In production, we'd fetch the ID dynamically, but let's use yours for now.
    account_id = "5OS80995"
    url = f"https://api.public.com/userapigateway/trading/accounts/{account_id}/portfolio/v2"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        # 3. Parse the data into a clean dictionary
        summary = {
            "cash": data['buyingPower']['cashOnlyBuyingPower'],
            "total_equity": sum(float(e['value']) for e in data['equity']),
            "stocks": []
        }

        for p in data.get('positions', []):
            summary['stocks'].append({
                "ticker": p['instrument']['symbol'],
                "shares": p['quantity'],
                "value": p['current_value' if 'current_value' in p else 'currentValue'],
                "gain_pct": p['instrumentGain']['gainPercentage']
            })

        return summary
    except Exception as e:
        st.error(f"Parsing Error: {e}")
        return None