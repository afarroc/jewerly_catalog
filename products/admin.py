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

class ProductAdminForm(ModelForm):
    """Custom form for Product admin to handle file uploads."""
    class Meta:
        model = Product
        fields = '__all__'

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'jewelry_type', 'material', 'price', 'stock', 'available', 'image_preview')
    list_filter = ('available', 'jewelry_type', 'material', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'available')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Características', {
            'fields': ('jewelry_type', 'material', 'category')
        }),
        ('Imagen', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Inventario y Precio', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        """Show image preview in list view."""
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 50px;" />'
        return "No image"
    image_preview.short_description = 'Image'
    image_preview.allow_tags = True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        logger.info(f"Product '{obj.name}' was {'updated' if change else 'created'} by {request.user}")

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)