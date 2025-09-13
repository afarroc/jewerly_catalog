# products/admin.py
from django.contrib import admin
from django.forms import ModelForm
from .models import Category, Product
import logging

logger = logging.getLogger(__name__)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        logger.info(f"Category '{obj.name}' was {'updated' if change else 'created'} by {request.user}")

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'jewelry_type', 'material', 'price', 'stock', 'available')
    list_filter = ('available', 'jewelry_type', 'material', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'available')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        logger.info(f"Product '{obj.name}' was {'updated' if change else 'created'} by {request.user}")

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)