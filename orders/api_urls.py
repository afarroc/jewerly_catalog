from django.urls import path
from . import views

app_name = 'orders_api'

urlpatterns = [
    path('list/', views.OrderListAPIView.as_view(), name='api_order_list'),
    path('detail/<str:order_number>/', views.OrderDetailAPIView.as_view(), name='api_order_detail'),
    path('cancel/<str:order_number>/', views.cancel_order_api, name='api_cancel_order'),
    path('history/', views.order_history_api, name='api_order_history'),
]