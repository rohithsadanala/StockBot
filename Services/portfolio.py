import requests
from .config_loader import get_config


def get_public_holdings():

    api_url = "https://api.public.com/v1/portfolios"
    headers = {
        "Authorization": f"Bearer {get_config('PUBLIC_API_KEY')}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            holdings = [item['symbol'] for item in data['items']]
            return holdings
        else:
            print(f"Error: Received status {response.status_code}")
            return []

    except Exception as e:
        print(f"Connection Error: {e}")
        return []