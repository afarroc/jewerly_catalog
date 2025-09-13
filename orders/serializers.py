from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model."""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_image_url = serializers.SerializerMethodField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_slug',
            'product_image_url', 'quantity', 'price', 'total_price'
        ]
        read_only_fields = ['id']

    def get_product_image_url(self, obj):
        """Get full URL for product image."""
        if obj.product.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product.image.url)
            return obj.product.image.url
        return None


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    is_paid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_email', 'user_name',
            'status', 'created_at', 'updated_at', 'subtotal', 'tax',
            'shipping_cost', 'total', 'shipping_address', 'billing_address',
            'payment_method', 'payment_status', 'payment_date',
            'tracking_number', 'notes', 'items', 'items_count', 'is_paid'
        ]
        read_only_fields = [
            'id', 'order_number', 'created_at', 'updated_at',
            'user', 'user_email', 'user_name', 'items_count', 'is_paid'
        ]

    def get_user_name(self, obj):
        """Get user's full name."""
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

    def get_items_count(self, obj):
        """Get total number of items in order."""
        return sum(item.quantity for item in obj.items.all())


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders."""
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'shipping_address', 'billing_address', 'payment_method',
            'notes', 'items'
        ]

    def create(self, validated_data):
        """Create order with items."""
        from django.db import transaction
        from decimal import Decimal

        items_data = validated_data.pop('items')
        user = self.context['request'].user

        # Calculate totals
        subtotal = Decimal('0.00')
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            subtotal += product.price * item_data['quantity']

        tax_rate = Decimal('0.08')  # 8%
        shipping_cost = Decimal('5.00')

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                subtotal=subtotal,
                tax=subtotal * tax_rate,
                shipping_cost=shipping_cost,
                total=subtotal + (subtotal * tax_rate) + shipping_cost,
                **validated_data
            )

            # Create order items
            for item_data in items_data:
                product = Product.objects.get(id=item_data['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data['quantity'],
                    price=product.price
                )

        return order


class OrderListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for order listings."""
    user_name = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()
    is_paid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user_name', 'status',
            'created_at', 'total', 'payment_status', 'is_paid',
            'items_count'
        ]

    def get_user_name(self, obj):
        """Get user's full name."""
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username

    def get_items_count(self, obj):
        """Get total number of items in order."""
        return sum(item.quantity for item in obj.items.all())