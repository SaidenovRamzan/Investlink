import os
import requests
import base64
from dotenv import load_dotenv
from order_management.serializers import ListOrdersQueryParametersSerializer


load_dotenv()


def alpaca_get_list_orders(account_id:int, params:dict) -> dict:
    """Get list from Alpaca api"""
    
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')
    credentials = f"{api_key}:{api_secret}"
    url = f"https://broker-api.sandbox.alpaca.markets/v1/trading/accounts/{account_id}/orders"

    base64_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "accept": "application/json",
        "authorization": f"Basic {base64_credentials}"
    }
    data = requests.get(url, headers=headers, params=params)
    return data.json()


def search_by_query_parameters(request, account_id:str)-> dict:
    """Accepts a request, account_id and returns a dictionary with data if all parameters are valid; 
    otherwise, returns a dictionary with errors"""

    response = {}
    serializer = ListOrdersQueryParametersSerializer(data=request.query_params)
    
    if serializer.is_valid():
        query_params = {
            'status': serializer.validated_data['status'],
            'limit': serializer.validated_data['limit'],
            'after': serializer.validated_data['after'],
            'until': serializer.validated_data['until'],
            'direction': serializer.validated_data['direction'],
            'nested': serializer.validated_data['nested'],
            'symbols': serializer.validated_data['symbols'],
            'qty_above': str(serializer.validated_data['qty_above'])\
                            if serializer.validated_data['qty_above']\
                             else '-1',
            'qty_below': str(serializer.validated_data['qty_below'])\
                            if serializer.validated_data['qty_below']\
                            else '100000000000000000000',
        }
        response = alpaca_get_list_orders(account_id=account_id, params=query_params)
    else: 
        response['errors'] = {key:value for key, value in serializer.errors.items()}
        
    return response
