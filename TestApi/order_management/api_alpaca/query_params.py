import os
import requests
import base64
from dotenv import load_dotenv
from order_management.serializers import ListOrdersQueryParametersSerializer
import logging

load_dotenv()


def alpaca_api_get_list_orders(account_id:int, params:dict) -> dict:
    """Get list from Alpaca API"""

    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')
    credentials = f"{api_key}:{api_secret}"
    url = f"https://broker-api.sandbox.alpaca.markets/v1/trading/accounts/{account_id}/orders"

    base64_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "accept": "application/json",
        "authorization": f"Basic Q0s3NlFMWEZRUlFONEMxSzAxMTc6Qm1LdTZpT0t6V0lnQmhaaDhBYTRnVHlGdXhxYTFtMjZZZGtTTFA1eA=="
    }
    data = requests.get(url, headers=headers, params=params)
    
    return data.json()


def search_by_query_parameters(request, account_id:str)-> dict:
    """Accepts a request, account_id and returns a dictionary with data if all parameters are valid; 
    otherwise, returns a dictionary with errors"""

    response = {}
    logging.info(f"{request.query_params=}==============================================")
    serializer = ListOrdersQueryParametersSerializer(data=request.query_params)
    
    if serializer.is_valid():
        query_params = {key:value for key, value in serializer.validated_data.items() if value}
        response = alpaca_api_get_list_orders(account_id=account_id, params=query_params)
        logging.info(f"{response=}40 in query after get=========================")
        # if response.get('message') in"forbidden.":
        #     response['errors'] = 'forbidden'
    else: 
        response['errors'] = {key:value for key, value in serializer.errors.items()}
        
    return response



