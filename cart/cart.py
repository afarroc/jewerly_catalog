from decimal import Decimal
from django.conf import settings
from products.models import Product

class CartItemsIterator:
    """Iterator for cart items that provides .all() method for template compatibility."""

    def __init__(self, cart_session):
        self.cart_session = cart_session

    def all(self):
        """Return all items in the cart."""
        return self.cart_session

    def __iter__(self):
        return self.cart_session.__iter__()

class CartSession:
    """Shopping cart stored in session for anonymous users."""

    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        # Ensure we don't exceed stock
        if self.cart[product_id]['quantity'] > product.stock:
            self.cart[product_id]['quantity'] = product.stock

        self.save()

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and get the products from the database."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids, available=True)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate the total cost of the items in the cart."""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """Remove the cart from session."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        """Mark the session as modified to make sure it gets saved."""
        self.session.modified = True

    # Properties to match the database cart interface
    @property
    def total_items(self):
        """Return total quantity of items in cart."""
        return self.__len__()

    @property
    def subtotal(self):
        """Calculate subtotal for all items in cart."""
        return self.get_total_price()

    @property
    def items(self):
        """Return cart items for template compatibility."""
        return CartItemsIterator(self)

    def add_product(self, product, quantity=1):
        """Add a product to the cart (compatibility method)."""
        self.add(product, quantity)

    def remove_product(self, product):
        """Remove a product from the cart (compatibility method)."""
        self.remove(product)