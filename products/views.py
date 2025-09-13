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
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Category, Product, ImageUpload
from .forms import ProductSearchForm, ProductForm, SimpleImageUploadForm
from .serializers import (
    CategorySerializer, ProductSerializer,
    ProductListSerializer
)
import logging

logger = logging.getLogger('products')
api_logger = logging.getLogger('api')
cache_logger = logging.getLogger('cache')
image_logger = logging.getLogger('image_upload')


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
            return redirect('products:product_detail', id=product.id, slug=product.slug)
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
            return redirect('products:product_detail', id=product.id, slug=product.slug)
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
    """View for deleting products and their associated image files."""
    user = request.user.username or 'Anonymous'

    try:
        product = get_object_or_404(Product, id=product_id)
        product_name = product.name
        has_image = bool(product.image and product.image.name)
        image_file = product.image.name if has_image else 'No image'

        if request.method == 'POST':
            logger.warning(f"[DELETE] Starting deletion process for product: ID={product_id}, Name='{product_name}', Image='{image_file}', User={user}")

            try:
                # Django automatically handles file deletion for ImageField when model is deleted
                product.delete()

                logger.info(f"[SUCCESS] Product deleted successfully: ID={product_id}, Name='{product_name}', User={user}")
                if has_image:
                    logger.info(f"[FILE] Associated image file also deleted: '{image_file}', User={user}")

                messages.success(request, f'Producto "{product_name}" eliminado exitosamente.')
                return redirect('products:product_list')

            except Exception as e:
                logger.error(f"[ERROR] Error deleting product ID={product_id}: {str(e)}, User={user}")
                messages.error(request, 'Error al eliminar el producto. Intente nuevamente.')

        else:
            logger.info(f"[CONFIRM] GET request to delete confirmation for product: ID={product.id}, Name='{product.name}', User={user}")

        context = {
            'product': product,
            'title': f'Eliminar Producto: {product.name}'
        }
        return render(request, 'products/product_confirm_delete.html', context)

    except Product.DoesNotExist:
        logger.error(f"[ERROR] Attempted to delete non-existent product: ID={product_id}, User={user}")
        messages.error(request, 'El producto que intenta eliminar no existe.')
        return redirect('products:product_list')
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error in product_delete for ID={product_id}: {str(e)}, User={user}")
        messages.error(request, 'Error inesperado al procesar la eliminación.')
        return redirect('products:product_list')


# Simple Image Upload Views
@login_required
def image_upload(request):
    """Simple view for uploading images."""
    user = request.user.username or 'Anonymous'

    if request.method == 'POST':
        image_logger.info(f"[UPLOAD] POST request to image_upload by user: {user}")
        form = SimpleImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                image_upload = form.save()
                file_size = image_upload.image.size if image_upload.image else 0
                file_name = image_upload.image.name if image_upload.image else 'No file'

                image_logger.info(f"[SUCCESS] Image uploaded successfully: ID={image_upload.id}, Title='{image_upload.title}', File='{file_name}', Size={file_size} bytes, User={user}")
                messages.success(request, f'Imagen "{image_upload.title}" subida exitosamente.')
                return redirect('products:image_list')
            except Exception as e:
                image_logger.error(f"[ERROR] Error saving image upload: {str(e)}, User={user}")
                messages.error(request, 'Error al guardar la imagen. Intente nuevamente.')
        else:
            image_logger.warning(f"[WARNING] Invalid form submission in image_upload: {form.errors}, User={user}")
            for field, errors in form.errors.items():
                for error in errors:
                    image_logger.warning(f"   Field '{field}': {error}")
    else:
        image_logger.debug(f"[PAGE] GET request to image_upload page by user: {user}")

    form = SimpleImageUploadForm()
    context = {
        'form': form,
        'title': 'Subir Imagen',
        'button_text': 'Subir Imagen'
    }
    return render(request, 'products/image_upload.html', context)


@login_required
def image_list(request):
    """View for listing uploaded images with pagination and search."""
    user = request.user.username or 'Anonymous'
    start_time = timezone.now()

    # Get search query
    search_query = request.GET.get('q', '').strip()
    page = request.GET.get('page', '1')

    image_logger.info(f"[LIST] GET request to image_list by user: {user}, Page: {page}, Search: '{search_query}'")

    # Base queryset
    images = ImageUpload.objects.all()
    total_before_filter = images.count()

    # Apply search filter if query exists
    if search_query:
        images = images.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        image_logger.info(f"[SEARCH] Search applied: '{search_query}' - Found {images.count()} of {total_before_filter} images")

    # Order by upload date (newest first)
    images = images.order_by('-uploaded_at')

    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(images, 12)  # 12 images per page

    try:
        images_page = paginator.page(page)
        image_logger.debug(f"[PAGE] Page {page} loaded with {images_page.object_list.count()} images")
    except PageNotAnInteger:
        images_page = paginator.page(1)
        image_logger.warning(f"[WARNING] Invalid page number '{page}', defaulting to page 1")
    except EmptyPage:
        images_page = paginator.page(paginator.num_pages)
        image_logger.warning(f"[WARNING] Page {page} out of range, showing last page {paginator.num_pages}")

    # Statistics
    total_images = ImageUpload.objects.count()
    recent_uploads = ImageUpload.objects.filter(
        uploaded_at__gte=timezone.now() - timezone.timedelta(days=7)
    ).count()

    # Performance logging
    end_time = timezone.now()
    duration = (end_time - start_time).total_seconds() * 1000  # milliseconds
    image_logger.info(f"[PERF] Image list rendered in {duration:.2f}ms - Total: {total_images}, Recent: {recent_uploads}, Page: {images_page.number}/{paginator.num_pages}")

    context = {
        'images': images_page,
        'title': 'Imágenes Subidas',
        'search_query': search_query,
        'total_images': total_images,
        'recent_uploads': recent_uploads,
        'is_paginated': images_page.has_other_pages(),
        'page_obj': images_page,
    }
    return render(request, 'products/image_list.html', context)


@login_required
def image_detail(request, image_id):
    """View for displaying image details."""
    user = request.user.username or 'Anonymous'

    try:
        image = get_object_or_404(ImageUpload, id=image_id)
        file_size = image.image.size if image.image else 0
        file_name = image.image.name if image.image else 'No file'

        image_logger.info(f"[VIEW] Image detail viewed: ID={image.id}, Title='{image.title}', File='{file_name}', Size={file_size} bytes, User={user}")

        context = {
            'image': image,
            'title': f'Imagen: {image.title}'
        }
        return render(request, 'products/image_detail.html', context)

    except ImageUpload.DoesNotExist:
        image_logger.error(f"[ERROR] Image not found: ID={image_id}, User={user}")
        raise
    except Exception as e:
        image_logger.error(f"[ERROR] Error displaying image detail ID={image_id}: {str(e)}, User={user}")
        raise


@login_required
def image_delete(request, image_id):
    """View for deleting uploaded images and their files."""
    user = request.user.username or 'Anonymous'

    try:
        image = get_object_or_404(ImageUpload, id=image_id)
        file_size = image.image.size if image.image else 0
        file_name = image.image.name if image.image else 'No file'

        if request.method == 'POST':
            title = image.title
            image_id_deleted = image.id

            # Log before deletion
            image_logger.warning(f"[DELETE] Starting deletion process for image: ID={image_id_deleted}, Title='{title}', File='{file_name}', Size={file_size} bytes, User={user}")

            # Step 1: Delete the physical file first
            file_deleted = False
            if image.image and image.image.name:
                try:
                    # Get the storage backend
                    storage = image.image.storage

                    # Check if file exists
                    if storage.exists(image.image.name):
                        # Delete the file
                        storage.delete(image.image.name)
                        file_deleted = True
                        image_logger.info(f"[FILE] Physical file deleted: '{file_name}' from storage, User={user}")
                    else:
                        image_logger.warning(f"[WARNING] Physical file not found: '{file_name}' - may have been already deleted, User={user}")
                        file_deleted = True  # Consider it deleted since it doesn't exist
                except Exception as file_error:
                    image_logger.error(f"[ERROR] Error deleting physical file '{file_name}': {str(file_error)}, User={user}")
                    # Continue with database deletion even if file deletion fails

            # Step 2: Delete the database record
            try:
                image.delete()
                image_logger.info(f"[SUCCESS] Image record deleted from database: ID={image_id_deleted}, Title='{title}', User={user}")

                if file_deleted:
                    image_logger.info(f"[COMPLETE] Complete deletion successful: ID={image_id_deleted}, Title='{title}' (file + record), User={user}")
                else:
                    image_logger.warning(f"[WARNING] Database record deleted but file may still exist: ID={image_id_deleted}, Title='{title}', File='{file_name}', User={user}")

                messages.success(request, f'Imagen "{title}" eliminada exitosamente.')
                return redirect('products:image_list')

            except Exception as db_error:
                image_logger.error(f"[ERROR] Error deleting database record for image ID={image_id_deleted}: {str(db_error)}, User={user}")
                messages.error(request, 'Error al eliminar el registro de la imagen. El archivo puede haber sido eliminado.')
                return redirect('products:image_list')

        else:
            image_logger.info(f"[CONFIRM] GET request to delete confirmation for image: ID={image.id}, Title='{image.title}', File='{file_name}', User={user}")

        context = {
            'image': image,
            'title': f'Eliminar Imagen: {image.title}'
        }
        return render(request, 'products/image_confirm_delete.html', context)

    except ImageUpload.DoesNotExist:
        image_logger.error(f"[ERROR] Attempted to delete non-existent image: ID={image_id}, User={user}")
        messages.error(request, 'La imagen que intenta eliminar no existe.')
        return redirect('products:image_list')
    except Exception as e:
        image_logger.error(f"[ERROR] Unexpected error in image_delete for ID={image_id}: {str(e)}, User={user}")
        messages.error(request, 'Error inesperado al procesar la eliminación.')
        return redirect('products:image_list')