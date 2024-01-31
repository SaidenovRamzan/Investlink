import os
from dotenv import load_dotenv
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
from order_management.models import Order


load_dotenv()


class CreateOrderFailureTestCase(APITestCase):
    def test_create_order_failure_side(self):
        account_id = os.getenv('Broker_id')
        url = reverse('create_order', args=[account_id])
        data = {
            "type": "market",
            "time_in_force": "day",
            "symbol": "AAPL",
            "qty": "4.124"
        }
        
        client = APIClient()
        response = client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('side', response.data)
        self.assertEqual(response.data['side'], [ErrorDetail(string='This field is required.', code='required')])
        
    def test_create_order_failure_type(self):
        account_id = os.getenv('Broker_id')
        url = reverse('create_order', args=[account_id])
        data = {
            "side": "buy",
            "time_in_force": "day",
            "symbol": "AAPL",
            "qty": "4.124"
        }
        
        client = APIClient()
        response = client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)
        self.assertEqual(response.data['type'], [ErrorDetail(string='This field is required.', code='required')])
    
    def test_create_order_failure_time_in_force(self):
        account_id = os.getenv('Broker_id')
        url = reverse('create_order', args=[account_id])
        data = {
            "side": "buy",
            "type": "market",
            "symbol": "AAPL",
            "qty": "4.124"
        }
        
        client = APIClient()
        response = client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('time_in_force', response.data)
        self.assertEqual(response.data['time_in_force'], [ErrorDetail(string='This field is required.', code='required')])
        
    def test_create_order_failure_symbol(self):
        account_id = os.getenv('Broker_id')
        url = reverse('create_order', args=[account_id])
        data = {
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "qty": "4.124"
        }
        
        client = APIClient()
        response = client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('symbol', response.data)
        self.assertEqual(response.data['symbol'], [ErrorDetail(string='This field is required.', code='required')])
        
    def test_create_order_failure_qty(self):
        account_id = os.getenv('Broker_id')
        url = reverse('create_order', args=[account_id])
        data = {
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "symbol": "AAPL"
        }
        
        client = APIClient()
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
class ListOrdersTestCase(APITestCase):
    def test_list_orders_with_status_parameter(self):
        account_id = os.getenv('Broker_id')
        url = reverse('list_orders', args=[account_id])
        response = self.client.get(url, {'status': 'open'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class CancelOrderTestCase(APITestCase):
    def test_cancel_order(self):
        order_id = 123
        account_id = os.getenv('Broker_id')
        
        url = reverse('cancel_order', args=[account_id, order_id])
        response = self.client.delete(url)

    def test_cancel_nonexistent_order(self):
        order_id = 999
        account_id = 456

        url = reverse('cancel-order', args=[account_id, order_id])
        response = self.client.delete(url)
