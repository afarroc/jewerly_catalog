from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from accounts.models import User
from products.models import Product
import uuid
import logging

logger = logging.getLogger(__name__)

class Order(models.Model):
    """Model representing a customer order."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    billing_address = models.TextField(blank=True)
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES,
        default='credit_card'
    )
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    tracking_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        """Calculate total before saving."""
        if not self.order_number:
            self.order_number = self.generate_order_number()
        self.total = self.subtotal + self.tax + self.shipping_cost
        super().save(*args, **kwargs)
        logger.info(f"Order {self.order_number} saved/updated")

    @staticmethod
    def generate_order_number():
        """Generate unique order number."""
        timestamp = timezone.now().strftime('%Y%m%d')
        unique_id = uuid.uuid4().hex[:6].upper()
        return f"ORD-{timestamp}-{unique_id}"

    @property
    def is_paid(self):
        """Check if order is paid."""
        return self.payment_status and self.payment_date is not None

class OrderItem(models.Model):
    """Model representing an item in an order."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.order_number}"

    @property
    def total_price(self):
        return self.price * self.quantity

@receiver(pre_save, sender=Order)
def update_product_stock(sender, instance, **kwargs):
    """Update product stock when order status changes to processing."""
    if instance.id:
        original = Order.objects.get(id=instance.id)
        if original.status != 'processing' and instance.status == 'processing':
            for item in instance.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()
                logger.info(f"Reduced stock for product {product.id} by {item.quantity}")