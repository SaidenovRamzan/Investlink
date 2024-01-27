import os
import requests
import base64
from dotenv import load_dotenv
import logging


load_dotenv()


def search_by_query_parameters(request, account_id:str):
    status_param = request.query_params.get('status', 'open')
    limit_param = request.query_params.get('limit', 50)
    after_param = request.query_params.get('after', '2000-01-02T15:04:05Z')
    until_param = request.query_params.get('until', '2026-01-02T15:04:05Z')
    direction_param = request.query_params.get('direction', 'desc')
    nested_param = request.query_params.get('nested', False)
    symbols_param = request.query_params.get('symbols', 'AAPL%2CTSLA%2CMSFT')
    qty_above_param = request.query_params.get('qty_above', -10000000000000000)
    qty_below_param = request.query_params.get('qty_below', 1000000000000000000000)
    subtag_param = request.query_params.get('subtag')
    
    # Строим url
    url = f"https://broker-api.sandbox.alpaca.markets/v1/trading/accounts/{account_id}/orders"
    url += f"?limit={str(limit_param)}&status={status_param}&after={after_param}&until={until_param}"
    url += f"&direction={direction_param}&nested={nested_param}&symbols={symbols_param}"
    url += f"&qty_above={str(qty_above_param)}&qty_below={str(qty_below_param)}"
    if subtag_param:
            url += f"&subtag={str(subtag_param)}"
            
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')
    
    # Объединяем имя пользователя и пароль с помощью двоеточия
    credentials = f"{api_key}:{api_secret}"
    
    # Преобразуем строку в формат Base64
    base64_credentials = base64.b64encode(credentials.encode()).decode()
    
    # Полученный результат
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {base64_credentials}"
    }
    
    data = requests.get(url, headers=headers)
    response = data.json()
    return response