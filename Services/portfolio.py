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
        # Using your confirmed Account ID
        account_id = "5OS80995"
        url = f"https://api.public.com/userapigateway/trading/accounts/{account_id}/portfolio/v2"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        response = requests.get(url, headers=headers)
        data = response.json()

        # 3. Flexible Parsing (Defensive Programming)
        # We check for the key, and if it's missing, we provide a default empty dictionary {}
        bp_data = data.get('buyingPower', {})
        cash = bp_data.get('cashOnlyBuyingPower', "0.00")

        # Calculate Total Equity safely
        equity_list = data.get('equity', [])
        total_value = sum(float(e.get('value', 0)) for e in equity_list)

        summary = {
            "cash": cash,
            "total_equity": total_value,
            "stocks": []
        }

        # 4. Extract Positions safely
        for p in data.get('positions', []):
            instr = p.get('instrument', {})
            gain_data = p.get('instrumentGain', {})

            summary['stocks'].append({
                "ticker": instr.get('symbol', 'Unknown'),
                "name": instr.get('name', ''),
                "shares": p.get('quantity', '0'),
                "value": p.get('currentValue', '0.00'),
                "gain_pct": gain_data.get('gainPercentage', '0')
            })

        return summary

    except Exception as e:
        # This will now tell us the EXACT line that failed
        st.error(f"Logic Error in Portfolio Sync: {e}")
        return None