from django.contrib.auth.models import AbstractUser
from django.db import models
import logging

logger = logging.getLogger(__name__)

class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    is_customer = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            logger.info(f"New user created: {self.username}")
        else:
            logger.debug(f"User updated: {self.username}")