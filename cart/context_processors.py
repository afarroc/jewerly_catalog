from .models import Cart

def cart(request):
    """Make the cart available globally in templates."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {'cart': cart}
    return {'cart': None}