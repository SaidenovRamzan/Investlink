import base64
import requests
import os

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer
from dotenv import load_dotenv
import logging
from order_management.query_params import search_by_query_parameters


load_dotenv()


class CreateOrder(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListOrders(APIView):
    def get(self, request, account_id,  *args, **kwargs):
        # Сериализация и отправка ответа
        order_data = search_by_query_parameters(request=request, account_id=account_id)
        if isinstance(order_data, dict):
            return Response(data={"code": 404, "message": "qty_above format invalid"},status=status.HTTP_404_NOT_FOUND)
            
        serializer = OrderSerializer(data=order_data,many=True)
        # Если нет этого заказа в бд то сохраняем
        if serializer.is_valid():
            for order_data in serializer.data:
                order_id = order_data.get('id')
                if not Order.objects.filter(id=order_id).exists():
                    Order.objects.create(**order_data)
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
    