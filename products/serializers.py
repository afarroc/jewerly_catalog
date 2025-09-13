from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description',
            'created_at', 'updated_at', 'products_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_products_count(self, obj):
        return obj.products.filter(available=True).count()


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    display_price = serializers.CharField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'display_price',
            'jewelry_type', 'material', 'category', 'category_name',
            'stock', 'available', 'created_at', 'updated_at', 'image', 'image_url'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'slug']

    def get_image_url(self, obj):
        """Get full URL for product image."""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def create(self, validated_data):
        """Create product with automatic slug generation."""
        if 'slug' not in validated_data or not validated_data['slug']:
            from django.utils.text import slugify
            validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update product with slug regeneration if name changed."""
        if 'name' in validated_data and validated_data['name'] != instance.name:
            from django.utils.text import slugify
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listings."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    display_price = serializers.CharField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'display_price',
            'jewelry_type', 'material', 'category_name',
            'available', 'image_url'
        ]

    def get_image_url(self, obj):
        """Get full URL for product image."""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None