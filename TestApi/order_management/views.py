from dotenv import load_dotenv
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from order_management.models import Order
from order_management.serializers import OrderSerializer, OrderCreateSerializer
import logging
from order_management import api_alpaca


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
        order_data = api_alpaca.search_by_query_parameters(request=request, account_id=account_id)
        serializer = OrderSerializer(data=order_data, many=True)
        
        if 'errors' in order_data:
            return Response(data={"code": 404, "message": f"{order_data['errors']}"},status=status.HTTP_404_NOT_FOUND)
        
        serializer.is_valid()
        return Response(serializer.data)

        
class CancelOrder(APIView):
    def delete(self, request, account_id, order_id):
        response = api_alpaca.alpaca_api_delete_order(
                    order_id=order_id,
                    account_id=account_id
        )
        logging.info(f"{response=}")
        if 204 not in response:
            return Response(data={"code": 404, "message": f"{response[1].decode()}"},status=status.HTTP_404_NOT_FOUND)
        
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
        except Order.DoesNotExist:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)
    