from dotenv import load_dotenv
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from order_management.models import Order
from order_management.serializers import OrderSerializer, OrderCreateSerializer
import logging
from order_management import api_alpaca


load_dotenv()


class CreateOrder(generics.CreateAPIView):
    """
    Create a new order.
    """
    serializer_class = OrderCreateSerializer
    
    @swagger_auto_schema(
        request_body=OrderCreateSerializer,
        responses={
            201: openapi.Response('Successful creation', OrderSerializer),
            400: 'Bad Request'
        }
    )    
    
    def post(self, request, account_id, **kwargs):
        """
        Create a new order.

        Parameters:
        - request (Request): HTTP request object containing data for creating the order.
        - account_id (int): The ID of the account for which the order is created.
        
        Returns:
        - Response: HTTP 201 Created with the newly created order data if successful,
                    HTTP 400 Bad Request if there is an error in the request.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = api_alpaca.alpaca_api_create_order(account_id, data=serializer.data)
        
        if response.get('code'):
            error_message = response.get("message")
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        order_serializer = OrderSerializer(data=response)
        
        if order_serializer.is_valid():
            Order.objects.create(**order_serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class ListOrders(APIView):
    """
    Retrieve a list of orders based on query parameters.
    """
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, description="Status of orders", type=openapi.TYPE_STRING),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Limit number of orders", type=openapi.TYPE_INTEGER),
            openapi.Parameter('after', openapi.IN_QUERY, description="Date after which orders were placed", type=openapi.TYPE_STRING, format='date-time'),
            openapi.Parameter('until', openapi.IN_QUERY, description="Date until which orders were placed", type=openapi.TYPE_STRING, format='date-time'),
            openapi.Parameter('direction', openapi.IN_QUERY, description="Direction of sorting", type=openapi.TYPE_STRING),
            openapi.Parameter('nested', openapi.IN_QUERY, description="Nested orders", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('symbols', openapi.IN_QUERY, description="Symbols of orders", type=openapi.TYPE_STRING),
            openapi.Parameter('qty_above', openapi.IN_QUERY, description="Quantity above", type=openapi.TYPE_INTEGER),
            openapi.Parameter('qty_below', openapi.IN_QUERY, description="Quantity below", type=openapi.TYPE_INTEGER),
            openapi.Parameter('subtag', openapi.IN_QUERY, description="Subtag", type=openapi.TYPE_STRING),
        ],
        responses={
            200: "List of orders",
            404: "Orders not found"
        }
    )
    def get(self, request, account_id):
        """
        Retrieve a list of orders based on query parameters.

        Parameters:
        - account_id (int): The ID of the account for which orders are retrieved.

        Returns:
        - Response: HTTP 200 OK with a list of orders if found,
                    HTTP 404 Not Found if no orders are found.
        """
        order_data = api_alpaca.search_by_query_parameters(request=request, account_id=account_id)
        serializer = OrderSerializer(data=order_data, many=True)
        
        if 'errors' in order_data:
            return Response(data={"code": 404, "message": f"{order_data['errors']}"},status=status.HTTP_404_NOT_FOUND)
        
        serializer.is_valid()
        return Response(serializer.data)

        
class CancelOrder(APIView):
    """
    Cancel an existing order.
    """

    @swagger_auto_schema(
        responses={
            204: "Order successfully canceled",
            404: "Order not found"
        }
    )
    def delete(self, request, account_id, order_id):
        """
        Cancel an existing order by its ID.

        Parameters:
        - account_id (int): The ID of the account associated with the order.
        - order_id (int): The ID of the order to cancel.

        Returns:
        - Response: HTTP 204 No Content if the order was successfully canceled,
                    HTTP 404 Not Found if the order was not found.
        """
        
        response = api_alpaca.alpaca_api_delete_order(
                    order_id=order_id,
                    account_id=account_id
        )
        if 204 not in response:
            return Response(data={"code": 404, "message": f"{response[1].decode()}"},status=status.HTTP_404_NOT_FOUND)
        
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
        except Order.DoesNotExist:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)
    