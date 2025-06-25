from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('webhooks/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('create-order/', views.create_order_ajax, name='create_order_ajax'),
    path('history/', views.order_history, name='order_history'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('invoice/<int:order_id>/', views.order_invoice, name='order_invoice'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms'),
]