# home/views.py
from django.shortcuts import render
from products.models import Product
from .models import Banner
import logging

logger = logging.getLogger(__name__)

def index(request):
    """Render the home page with banners and featured products."""
    try:
        # Obtener banners activos ordenados por prioridad
        active_banners = Banner.objects.filter(is_active=True).order_by('order', '-created_at')
        logger.debug(f"Mostrando {len(active_banners)} banners activos")

        # Obtener productos destacados
        featured_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
        logger.debug(f"Mostrando {len(featured_products)} productos destacados")

    except Exception as e:
        active_banners = []
        featured_products = []
        logger.error(f"Error al obtener datos para la página de inicio: {str(e)}")

    context = {
        'title': 'Catálogo de Joyería Fantasía',
        'welcome_message': '¡Bienvenido a nuestra Colección de Joyería Fantasía!',
        'banners': active_banners,
        'featured_products': featured_products,
    }
    return render(request, 'home/index.html', context)