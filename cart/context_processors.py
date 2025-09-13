from .models import Cart
from .cart import CartSession

def cart(request):
    """Make the cart available globally in templates."""
    if request.user.is_authenticated:
        # Use database cart for authenticated users
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {'cart': cart}
    else:
        # Use session cart for anonymous users
        cart_session = CartSession(request)
        return {'cart': cart_session}