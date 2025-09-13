# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Category, Product
from .forms import ProductSearchForm, ProductForm
from .serializers import (
    CategorySerializer, ProductSerializer,
    ProductListSerializer
)
import logging

logger = logging.getLogger('products')
api_logger = logging.getLogger('api')
cache_logger = logging.getLogger('cache')


def product_list(request, category_slug=None):
    """Simple function-based view for displaying products."""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'search_form': ProductSearchForm(),
        'has_filters': False,
    }
    return render(request, 'products/product_list.html', context)


class ProductDetailView(DetailView):
    """Class-based view for displaying product details with caching."""
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    @method_decorator(cache_page(600))  # Cache for 10 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        """Only show available products with optimized queries."""
        return Product.objects.filter(available=True).select_related('category')

    def get_object(self, queryset=None):
        """Get product by id and slug for URL validation with caching."""
        if queryset is None:
            queryset = self.get_queryset()

        # Get both id and slug from URL
        product_id = self.kwargs.get('id')
        slug = self.kwargs.get('slug')

        # Try cache first
        cache_key = f'product_detail_{product_id}_{slug}'
        product = cache.get(cache_key)

        if product is None:
            # Validate that id and slug match
            product = get_object_or_404(
                queryset,
                id=product_id,
                slug=slug
            )
            # Cache the product
            cache.set(cache_key, product, 600)  # Cache for 10 minutes
            logger.debug(f"Cached product detail: {cache_key}")
        else:
            logger.debug(f"Cache hit for product detail: {cache_key}")

        logger.debug(f"Displaying product detail for: {product.name}")
        return product


# API Views
class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListAPIView(generics.ListCreateAPIView):
    """API view for listing and creating categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating and deleting categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListAPIView(generics.ListCreateAPIView):
    """API view for listing and creating products."""
    queryset = Product.objects.filter(available=True)
    permission_classes = [AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['category', 'jewelry_type', 'material', 'available']
    search_fields = ['name', 'description', 'jewelry_type', 'material']
    ordering_fields = ['name', 'price', 'created_at', 'updated_at']
    ordering = ['-created_at']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """Use different serializer for list vs create."""
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductSerializer


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating and deleting products."""
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


@api_view(['GET'])
@permission_classes([AllowAny])
def featured_products_api(request):
    """API endpoint for featured products."""
    products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    serializer = ProductListSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def products_by_category_api(request, category_slug):
    """API endpoint for products by category."""
    try:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category, available=True)
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response(
            {'error': 'Category not found'},
            status=status.HTTP_404_NOT_FOUND
        )


# Product Management Views (for admin/staff)
@login_required
def product_create(request):
    """View for creating new products with image upload."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Producto "{product.name}" creado exitosamente.')
            logger.info(f"Product created: {product.name} by user {request.user.username}")
            return redirect('product_detail', id=product.id, slug=product.slug)
    else:
        form = ProductForm()

    context = {
        'form': form,
        'title': 'Crear Nuevo Producto',
        'button_text': 'Crear Producto'
    }
    return render(request, 'products/product_form.html', context)


@login_required
def product_update(request, product_id):
    """View for updating existing products with image upload."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Producto "{product.name}" actualizado exitosamente.')
            logger.info(f"Product updated: {product.name} by user {request.user.username}")
            return redirect('product_detail', id=product.id, slug=product.slug)
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'title': f'Editar Producto: {product.name}',
        'button_text': 'Actualizar Producto'
    }
    return render(request, 'products/product_form.html', context)


@login_required
def product_delete(request, product_id):
    """View for deleting products."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Producto "{product_name}" eliminado exitosamente.')
        logger.info(f"Product deleted: {product_name} by user {request.user.username}")
        return redirect('product_list')

    context = {
        'product': product,
        'title': f'Eliminar Producto: {product.name}'
    }
    return render(request, 'products/product_confirm_delete.html', context)