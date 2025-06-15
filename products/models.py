# products/models.py
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
import logging

logger = logging.getLogger(__name__)

class Category(models.Model):
    """Model representing a product category."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Automatically create slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        logger.info(f"Category '{self.name}' saved")

class Product(models.Model):
    """Model representing a fantasy jewelry product."""
    JEWELRY_TYPES = [
        ('ring', 'Ring'),
        ('necklace', 'Necklace'),
        ('bracelet', 'Bracelet'),
        ('earring', 'Earring'),
        ('brooch', 'Brooch'),
        ('tiara', 'Tiara'),
        ('other', 'Other'),
    ]

    MATERIALS = [
        ('metal', 'Metal'),
        ('resin', 'Resin'),
        ('glass', 'Glass'),
        ('crystal', 'Crystal'),
        ('pearl', 'Pearl'),
        ('fabric', 'Fabric'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    jewelry_type = models.CharField(
        max_length=20,
        choices=JEWELRY_TYPES,
        default='other'
    )
    material = models.CharField(
        max_length=20,
        choices=MATERIALS,
        default='other'
    )
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Automatically create slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        logger.info(f"Product '{self.name}' saved")

    @property
    def display_price(self):
        """Format price for display with currency symbol."""
        return f"${self.price:.2f}"