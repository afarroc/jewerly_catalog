from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import Cart
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """Create a cart for each new user."""
    if created:
        Cart.objects.create(user=instance)
        logger.info(f"Cart created for new user: {instance.username}")