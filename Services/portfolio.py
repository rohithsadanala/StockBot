import requests
import streamlit as st


def get_detailed_portfolio():
    secret_key = st.secrets["PUBLIC_API_KEY"]

    # 1. Get Access Token
    auth_url = "https://api.public.com/userapiauthservice/personal/access-tokens"
    try:
        auth_res = requests.post(auth_url, json={"validityInMinutes": 60, "secret": secret_key})
        token = auth_res.json().get("accessToken")

        # 2. Get Portfolio V2
        account_id = "5OS80995"
        url = f"https://api.public.com/userapigateway/trading/accounts/{account_id}/portfolio/v2"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        response = requests.get(url, headers=headers)
        data = response.json()

        # --- THE DEBUGGER ---
        # If you see an error, uncomment the line below to see the raw JSON on your website
        # st.write("RAW DATA:", data)

        # 3. Flexible Parsing (Handles both camelCase and snake_case)
        # We look for the data in multiple possible keys
        bp = data.get('buyingPower') or data.get('buying_power') or {}
        cash = bp.get('cashOnlyBuyingPower') or bp.get('cash_only_buying_power') or "0.00"

        equity_data = data.get('equity') or data.get('equity_summary') or []
        total_value = sum(float(e.get('value', 0)) for e in equity_data) if isinstance(equity_data, list) else 0

        summary = {
            "cash": cash,
            "total_equity": total_value,
            "stocks": []
        }

        # 4. Extract Positions safely
        for p in data.get('positions', []):
            instr = p.get('instrument', {})
            gain_data = p.get('instrumentGain') or p.get('instrument_gain') or {}

            summary['stocks'].append({
                "ticker": instr.get('symbol', 'Unknown'),
                "shares": p.get('quantity', '0'),
                "gain_pct": gain_data.get('gainPercentage') or gain_data.get('gain_percentage') or "0"
            })

        return summary

    except Exception as e:
        st.error(f"Logic Error: {e}")
        return None