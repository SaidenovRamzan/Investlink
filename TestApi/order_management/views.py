from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from order_management.models import Order
from order_management.serializers import OrderSerializer, OrderCreateSerializer
from dotenv import load_dotenv
import logging
from order_management import api_alpaca, tasks 


load_dotenv()


class CreateOrder(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    
    def post(self, request, account_id, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logging.info(f"{serializer.data=}")
        logging.info(f"{serializer.errors=}")
        response = api_alpaca.alpaca_api_create_order(account_id, data=serializer.data)
        
        if response.get('code'):
            error_message = response.get("message")
            logging.info(f"{response=}")
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        logging.info(f"{response=}")
        order_serializer = OrderSerializer(data=response)
        
        if order_serializer.is_valid():
            Order.objects.create(**order_serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class ListOrders(APIView):
    def get(self, request, account_id):
        logging.info(f"===================================================================================")
        tasks.listen_sse_events.delay()
        logging.info(f"=============TASK WORK======================================================================")
        
        # Получение данных
        order_data = api_alpaca.search_by_query_parameters(request=request, account_id=account_id)
        logging.info(f'{order_data=} in view 42')
        
        serializer = OrderSerializer(data=order_data,many=True)
        if 'errors' in order_data:
            return Response(data={"code": 404, "message": f"{order_data['errors']}"},status=status.HTTP_404_NOT_FOUND)
        serializer.is_valid()
        # Если нет этого заказа в бд то сохраняемss
        if serializer.is_valid():
            for order_data in serializer.data:
                order_id = order_data.get('id')
                
                if not Order.objects.filter(id=order_id).exists():
                    Order.objects.create(**order_data)
        logging.info(serializer)
        return Response(serializer.data)

        
class CancelOrder(APIView):
    def delete(self, request, order_id):
        
        try:
            order = Order.objects.get(id=order_id)
            
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    