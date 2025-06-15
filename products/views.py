# products/views.py
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
import logging

logger = logging.getLogger(__name__)

def product_list(request, category_slug=None):
    """Display all products or products filtered by category."""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        logger.debug(f"Displaying products for category: {category.name}")
    else:
        logger.debug("Displaying all available products")
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, id, slug):
    """Display detailed information about a single product."""
    product = get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True
    )
    logger.debug(f"Displaying product detail for: {product.name}")
    
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)