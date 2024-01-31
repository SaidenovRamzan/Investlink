import requests


def alpaca_api_create_order(account_id:int, data):
    url = f"https://broker-api.sandbox.alpaca.markets/v1/trading/accounts/{account_id}/orders"

    payload = {key : value for key, value in data.items() if value}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic Q0s3NlFMWEZRUlFONEMxSzAxMTc6Qm1LdTZpT0t6V0lnQmhaaDhBYTRnVHlGdXhxYTFtMjZZZGtTTFA1eA=="
    }

    response = requests.post(url, json=payload, headers=headers)

    return (response.json())