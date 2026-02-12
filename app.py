import streamlit as st
from main import run_live_analysis # Your File 6 logic
from Services.config_loader import get_config
from Services.portfolio import get_detailed_portfolio
import re
import requests

def get_detailed_portfolio():
    secret_key = st.secrets["PUBLIC_API_KEY"]

    # 1. Get Access Token
    auth_url = "https://api.public.com/userapiauthservice/personal/access-tokens"
    auth_res = requests.post(auth_url, json={"validityInMinutes": 60, "secret": secret_key})
    token = auth_res.json().get("accessToken")

    # 2. Get Portfolio (Using your account ID)
    account_id = "5OS80995"
    url = f"https://api.public.com/userapigateway/trading/accounts/{account_id}/portfolio/v2"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        # --- DEBUG: See the real structure in Streamlit if it fails ---
        # st.write(data) # Uncomment this line if you want to see the full JSON on screen

        # 3. Parse Safely
        # We use .get() so it returns 0 instead of crashing if 'buyingPower' is missing
        bp_data = data.get('buyingPower', {})
        cash = bp_data.get('cashOnlyBuyingPower', "0.00")

        # Calculate Total Equity from the equity list
        equity_list = data.get('equity', [])
        total_value = sum(float(e.get('value', 0)) for e in equity_list)

        summary = {
            "cash": cash,
            "total_equity": total_value,
            "stocks": []
        }

        # 4. Extract Positions
        for p in data.get('positions', []):
            instr = p.get('instrument', {})
            summary['stocks'].append({
                "ticker": instr.get('symbol', 'Unknown'),
                "shares": p.get('quantity', '0'),
                "gain_pct": p.get('instrumentGain', {}).get('gainPercentage', '0')
            })

        return summary

    except Exception as e:
        st.error(f"Detailed Parsing Error: {e}")
        return None