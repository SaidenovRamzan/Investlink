from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='order')


urlpatterns = [
    path('create/<str:account_id>/order', views.CreateOrder.as_view(), name='create_order'),
    path('list/<str:account_id>/orders', views.ListOrders.as_view(), name='list_orders'),
    path('cancel/<str:order_id>/', views.CancelOrder.as_view(), name='cancel_order'),
    path('', include(router.urls)),
]
