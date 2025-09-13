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
    list_display = ('name', 'jewelry_type', 'material', 'price', 'stock', 'available', 'image_preview', 'created_at')
    list_display_links = ('name', 'image_preview')
    list_filter = ('available', 'jewelry_type', 'material', 'category', 'created_at')
    search_fields = ('name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'available')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25

    # Actions en lote
    actions = ['make_available', 'make_unavailable', 'export_csv']

    def make_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f'{updated} productos marcados como disponibles.')
    make_available.short_description = 'Marcar productos como disponibles'

    def make_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f'{updated} productos marcados como no disponibles.')
    make_unavailable.short_description = 'Marcar productos como no disponibles'

    def export_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="productos.csv"'

        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Tipo', 'Material', 'Precio', 'Stock', 'Disponible'])

        for product in queryset:
            writer.writerow([
                product.name,
                product.get_jewelry_type_display(),
                product.get_material_display(),
                product.price,
                product.stock,
                'Sí' if product.available else 'No'
            ])

        self.message_user(request, f'Exportados {queryset.count()} productos a CSV.')
        return response
    export_csv.short_description = 'Exportar productos a CSV'

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
            try:
                return f'''
                <div style="text-align: center;">
                    <img src="{obj.image.url}" style="max-height: 50px; max-width: 50px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />
                    <br><small style="color: #666;">{obj.name[:20]}...</small>
                </div>
                '''
            except:
                return '<span style="color: #dc3545;">Error loading image</span>'
        return '<span style="color: #6c757d;">No image</span>'
    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        logger.info(f"Product '{obj.name}' was {'updated' if change else 'created'} by {request.user}")

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)