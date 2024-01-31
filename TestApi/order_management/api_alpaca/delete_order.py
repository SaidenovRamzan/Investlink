import os
import requests
import base64
from dotenv import load_dotenv
import logging

load_dotenv()


def alpaca_api_delete_order(account_id:str, order_id:str) -> None:
    """Get list from Alpaca API"""

    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')
    credentials = f"{api_key}:{api_secret}"
    url = f"https://broker-api.sandbox.alpaca.markets/v1/trading/accounts/{account_id}/orders/{order_id}"

    base64_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "accept": "application/json",
        "authorization": f"Basic Q0s3NlFMWEZRUlFONEMxSzAxMTc6Qm1LdTZpT0t6V0lnQmhaaDhBYTRnVHlGdXhxYTFtMjZZZGtTTFA1eA=="
    }
    data = requests.delete(url, headers=headers)
    
    return (data.status_code, data.content)
