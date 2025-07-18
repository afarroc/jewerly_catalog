# home/views.py
from django.shortcuts import render
from products.models import Product
import logging

logger = logging.getLogger(__name__)

def index(request):
    """Render the home page with featured products."""
    try:
        featured_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
        logger.debug(f"Mostrando {len(featured_products)} productos destacados en la página de inicio")
    except Exception as e:
        featured_products = []
        logger.error(f"Error al obtener productos destacados: {str(e)}")

    context = {
        'title': 'Catálogo de Joyería Fantasía',
        'welcome_message': '¡Bienvenido a nuestra Colección de Joyería Fantasía!',
        'featured_products': featured_products,
    }
    return render(request, 'home/index.html', context)