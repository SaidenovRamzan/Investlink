from django.urls import path
from . import views


urlpatterns = [
    path('create/<str:account_id>/order', views.CreateOrder.as_view(), name='create_order'),
    path('list/<str:account_id>/orders', views.ListOrders.as_view(), name='list_orders'),
    path('cancel/<str:account_id>/<str:order_id>', views.CancelOrder.as_view(), name='cancel_order'),
]
