from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from dotenv import load_dotenv
import logging
import datetime
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
        # Получение данных
        order_data = api_alpaca.search_by_query_parameters(request=request, account_id=account_id)
        serializer = OrderSerializer(data=order_data,many=True)

        if 'errors' in order_data:
            return Response(data={"code": 404, "message": f"{order_data['errors']}"},status=status.HTTP_404_NOT_FOUND)
            
        # Если нет этого заказа в бд то сохраняем
        if serializer.is_valid():
            for order_data in serializer.data:
                order_id = order_data.get('id')
                if not Order.objects.filter(id=order_id).exists():
                    order = Order.objects.create(**order_data)
        times = datetime.datetime.strptime(str('2060-03-16T18:38:01.942282Z'), '%Y-%m-%dT%H:%M:%S.%fZ')
        
        logging.info(f"{order_data=}") 
        logging.info(f"{times=}") 
        logging.info(f'{times.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}')      
             
        return Response(serializer.data)

        
class CancelOrder(APIView):
    def delete(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', 'open')
        limit = int(self.request.query_params.get('limit', 50))
        after = self.request.query_params.get('after', None)
        until = self.request.query_params.get('until', None)
        direction = self.request.query_params.get('direction', 'desc')
        nested = self.request.query_params.get('nested', False)
        symbols = self.request.query_params.get('symbols', None)
        qty_above = self.request.query_params.get('qty_above', None)
        qty_below = self.request.query_params.get('qty_below', None)
        subtag = self.request.query_params.get('subtag', None)

        # Применяем фильтры к queryset
        if status:
            queryset = queryset.filter(status=status)
        if after:
            queryset = queryset.filter(created_at__gt=after)
        if until:
            queryset = queryset.filter(created_at__lt=until)
        if symbols:
            queryset = queryset.filter(symbol__in=symbols.split(','))
        if qty_above:
            queryset = queryset.filter(quantity__gt=float(qty_above))
        if qty_below:
            queryset = queryset.filter(quantity__lt=float(qty_below))
        if subtag:
            queryset = queryset.filter(subtag=subtag)
        if nested:
            queryset = queryset.filter(nested=nested)

        # Управляем направлением сортировки
        if direction == 'asc':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        # Возвращаем результат
        return queryset[:limit]
    