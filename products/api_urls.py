from django.urls import path
from . import views

app_name = 'products_api'

urlpatterns = [
    path('list/', views.ProductListAPIView.as_view(), name='api_product_list'),
    path('detail/<slug:slug>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('categories/list/', views.CategoryListAPIView.as_view(), name='api_category_list'),
    path('categories/detail/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='api_category_detail'),
    path('featured/', views.featured_products_api, name='api_featured_products'),
    path('category/<slug:category_slug>/', views.products_by_category_api, name='api_products_by_category'),
]