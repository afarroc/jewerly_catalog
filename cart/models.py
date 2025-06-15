from django.db import models
from products.models import Product
from accounts.models import User
import logging

logger = logging.getLogger(__name__)

class Cart(models.Model):
    """Model representing a user's shopping cart."""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'

    def __str__(self):
        return f"Cart #{self.id} - {self.user.username}"

    @property
    def total_items(self):
        """Return total quantity of items in cart."""
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Calculate subtotal for all items in cart."""
        return sum(item.total_price for item in self.items.all())

    def add_product(self, product, quantity=1):
        """Add a product to the cart or update quantity if already exists."""
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        logger.info(f"Product {product.id} added to cart {self.id}")

    def remove_product(self, product):
        """Remove a product from the cart."""
        self.items.filter(product=product).delete()
        logger.info(f"Product {product.id} removed from cart {self.id}")

    def clear(self):
        """Remove all items from the cart."""
        self.items.all().delete()
        logger.info(f"Cart {self.id} cleared")

class CartItem(models.Model):
    """Model representing an item in the shopping cart."""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Cart #{self.cart.id}"

    @property
    def total_price(self):
        """Calculate total price for this cart item."""
        return self.product.price * self.quantity