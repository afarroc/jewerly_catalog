from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

@login_required
def cart_detail(request):
    """Display the contents of the shopping cart."""
    cart = get_object_or_404(Cart, user=request.user)
    context = {
        'title': 'Shopping Cart',
        'cart': cart,
    }
    return render(request, 'cart/cart_detail.html', context)

@login_required
def cart_add(request, product_id):
    """Add a product to the cart or increment quantity."""
    product = get_object_or_404(Product, id=product_id, available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        messages.warning(request, f"Only {product.stock} available in stock.")
        quantity = product.stock
    
    cart.add_product(product, quantity)
    messages.success(request, f"Added {product.name} to your cart.")
    logger.info(f"Product {product.id} added to cart {cart.id}")
    
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))

@login_required
def cart_remove(request, product_id):
    """Remove a product from the cart."""
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    
    cart.remove_product(product)
    messages.success(request, f"Removed {product.name} from your cart.")
    logger.info(f"Product {product.id} removed from cart {cart.id}")
    
    return redirect('cart:cart_detail')

@login_required
def cart_update(request, product_id):
    """Update the quantity of a product in the cart."""
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_object_or_404(Cart, user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        return cart_remove(request, product_id)
    
    if quantity > product.stock:
        messages.warning(request, f"Only {product.stock} available in stock.")
        quantity = product.stock
    
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.quantity = quantity
    cart_item.save()
    
    messages.success(request, f"Updated {product.name} quantity.")
    logger.info(f"Cart {cart.id} updated - Product {product.id} quantity set to {quantity}")
    
    return redirect('cart:cart_detail')

@login_required
def cart_clear(request):
    """Remove all items from the cart."""
    cart = get_object_or_404(Cart, user=request.user)
    cart.clear()
    messages.success(request, "Your cart has been cleared.")
    logger.info(f"Cart {cart.id} cleared by user")
    
    return redirect('cart:cart_detail')