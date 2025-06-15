# home/views.py
from django.shortcuts import render
from products.models import Product
import logging

logger = logging.getLogger(__name__)

def index(request):
    """Render the home page with featured products."""
    try:
        featured_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
        logger.debug(f"Displaying {len(featured_products)} featured products on home page")
    except Exception as e:
        featured_products = []
        logger.error(f"Error fetching featured products: {str(e)}")

    context = {
        'title': 'Fantasy Jewelry Catalog',
        'welcome_message': 'Welcome to our Fantasy Jewelry Collection!',
        'featured_products': featured_products,
    }
    return render(request, 'home/index.html', context)