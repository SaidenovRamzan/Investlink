import os
from dotenv import load_dotenv
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Order


load_dotenv()


class CreateOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_order_url = f"http://localhost:8000/create/{os.getenv('Broker_id')}/order"

    def test_create_order(self):
        payload = {
            'symbol': 'AAPL',
            'qty': '100',
            'side': 'buy',
            'type': 'market',
            'time_in_force': 'day',
        }
        response = self.client.post(self.create_order_url, payload, format='json')
        print(response.status_code, response, '='*20)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Дополнительные проверки, например, проверка создания объекта в базе данных
        # self.assertTrue(Order.objects.filter(...).exists())

# class ListOrdersTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.list_orders_url = reverse('list_orders')

#     def test_list_orders(self):
#         # Создайте несколько заказов, чтобы проверить список
#         # Сделайте запрос на получение списка заказов
#         response = self.client.get(self.list_orders_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Дополнительные проверки, например, проверка структуры данных в ответе

# class CancelOrderTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.cancel_order_url = reverse('cancel_order', args=[1, 1])  # Подставьте реальные аргументы

#     def test_cancel_order(self):
#         # Создайте заказ, который будет отменен во время теста
#         # Сделайте запрос на отмену заказа
#         response = self.client.delete(self.cancel_order_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#         # Дополнительные проверки, например, проверка отсутствия заказа после отмены
