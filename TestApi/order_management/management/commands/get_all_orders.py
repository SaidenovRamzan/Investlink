import requests
import base64
from django.core.management.base import BaseCommand
from order_management.models import Order
from order_management.serializers import OrderSerializer


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('GET request in Alpaca Api for geting all orders...'))
        url = "https://broker-api.sandbox.alpaca.markets/v1/trading/accounts/5e62581b-1a60-4f8d-a950-4efa12d15be7/orders?limit=10000&status=all"

        headers = {
            "accept": "application/json",
            "authorization": f"Basic Q0s3NlFMWEZRUlFONEMxSzAxMTc6Qm1LdTZpT0t6V0lnQmhaaDhBYTRnVHlGdXhxYTFtMjZZZGtTTFA1eA=="
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if isinstance(data, list):
            serializer = OrderSerializer(data=data,many=True)
            serializer.is_valid()
            
            for order_data in serializer.data:
                try:
                    order_id = order_data.get('id')

                    if not Order.objects.filter(id=order_id).exists():
                        Order.objects.create(**order_data)
                except:
                    pass