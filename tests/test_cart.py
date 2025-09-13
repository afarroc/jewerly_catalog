import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from cart.models import Cart, CartItem
from products.models import Product, Category
from decimal import Decimal


@pytest.mark.django_db
class TestCartModel:
    """Test cases for Cart model functionality."""

    def test_cart_creation(self, user):
        """Test that a cart is created for a user."""
        cart = Cart.objects.create(user=user)

        assert cart.user == user
        assert cart.total_items == 0
        assert cart.subtotal == 0
        assert str(cart) == f"Cart #{cart.id} - {user.username}"

    def test_cart_add_product_new(self, user, product):
        """Test adding a new product to cart."""
        cart = Cart.objects.create(user=user)

        # Add product to cart
        cart.add_product(product, 2)

        # Verify cart item was created
        cart_item = CartItem.objects.get(cart=cart, product=product)
        assert cart_item.quantity == 2
        assert cart_item.total_price == product.price * 2
        assert cart.total_items == 2
        assert cart.subtotal == product.price * 2

    def test_cart_add_product_existing(self, user, product):
        """Test adding quantity to existing product in cart."""
        cart = Cart.objects.create(user=user)

        # Add product first time
        cart.add_product(product, 1)
        assert cart.total_items == 1

        # Add same product again
        cart.add_product(product, 3)
        assert cart.total_items == 4

        # Verify only one cart item exists
        cart_items = CartItem.objects.filter(cart=cart, product=product)
        assert cart_items.count() == 1

        cart_item = cart_items.first()
        assert cart_item.quantity == 4

    def test_cart_remove_product(self, user, product):
        """Test removing a product from cart."""
        cart = Cart.objects.create(user=user)
        cart.add_product(product, 2)

        # Verify product is in cart
        assert cart.total_items == 2

        # Remove product
        cart.remove_product(product)

        # Verify product was removed
        assert cart.total_items == 0
        assert not CartItem.objects.filter(cart=cart, product=product).exists()

    def test_cart_clear(self, user, product):
        """Test clearing all items from cart."""
        cart = Cart.objects.create(user=user)
        cart.add_product(product, 5)

        # Verify cart has items
        assert cart.total_items == 5

        # Clear cart
        cart.clear()

        # Verify cart is empty
        assert cart.total_items == 0
        assert not CartItem.objects.filter(cart=cart).exists()

    def test_cart_multiple_products(self, user):
        """Test cart with multiple different products."""
        cart = Cart.objects.create(user=user)

        # Create multiple products
        category = Category.objects.create(name='Test', slug='test')
        product1 = Product.objects.create(
            name='Product 1', slug='product-1', price=Decimal('10.00'),
            category=category, stock=10
        )
        product2 = Product.objects.create(
            name='Product 2', slug='product-2', price=Decimal('20.00'),
            category=category, stock=10
        )

        # Add both products
        cart.add_product(product1, 2)
        cart.add_product(product2, 3)

        # Verify cart contents
        assert cart.total_items == 5
        assert cart.subtotal == Decimal('80.00')  # (2*10) + (3*20)

        # Verify cart items
        assert CartItem.objects.filter(cart=cart).count() == 2


@pytest.mark.django_db
class TestCartViews:
    """Test cases for cart views."""

    def test_cart_detail_authenticated(self, authenticated_client, user):
        """Test cart detail view for authenticated user."""
        # Create cart for user
        cart = Cart.objects.create(user=user)

        url = reverse('cart:cart_detail')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'cart' in response.context
        assert response.context['cart'] == cart

    def test_cart_detail_unauthenticated(self, api_client):
        """Test cart detail view for unauthenticated user."""
        url = reverse('cart:cart_detail')
        response = api_client.get(url)

        # Should redirect to login
        assert response.status_code == status.HTTP_302_FOUND
        assert 'login' in response.url

    def test_add_product_to_cart(self, authenticated_client, user, product):
        """Test adding product to cart via POST."""
        url = reverse('cart:cart_add', kwargs={'product_id': product.id})

        # Add product to cart
        response = authenticated_client.post(url, {'quantity': 3})

        # Should redirect back
        assert response.status_code == status.HTTP_302_FOUND

        # Verify product was added to cart
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        assert cart_item.quantity == 3

    def test_add_unavailable_product(self, authenticated_client, unavailable_product):
        """Test adding unavailable product to cart."""
        url = reverse('cart:cart_add', kwargs={'product_id': unavailable_product.id})

        response = authenticated_client.post(url, {'quantity': 1})

        # Should return 404 since product is not available
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_add_product_exceeds_stock(self, authenticated_client, user, product):
        """Test adding more products than available stock."""
        # Set product stock to 5
        product.stock = 5
        product.save()

        url = reverse('cart:cart_add', kwargs={'product_id': product.id})

        # Try to add 10 items (more than stock)
        response = authenticated_client.post(url, {'quantity': 10})

        # Should succeed but limit to available stock
        assert response.status_code == status.HTTP_302_FOUND

        # Verify only 5 items were added
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        assert cart_item.quantity == 5

    def test_update_cart_item(self, authenticated_client, user, product):
        """Test updating cart item quantity."""
        # Add product to cart first
        cart = Cart.objects.create(user=user)
        cart.add_product(product, 2)

        url = reverse('cart:cart_update', kwargs={'product_id': product.id})

        # Update quantity to 5
        response = authenticated_client.post(url, {'quantity': 5})

        assert response.status_code == status.HTTP_302_FOUND

        # Verify quantity was updated
        cart_item = CartItem.objects.get(cart=cart, product=product)
        assert cart_item.quantity == 5

    def test_update_cart_item_zero_quantity(self, authenticated_client, user, product):
        """Test updating cart item to zero quantity (should remove item)."""
        # Add product to cart first
        cart = Cart.objects.create(user=user)
        cart.add_product(product, 2)

        url = reverse('cart:cart_update', kwargs={'product_id': product.id})

        # Update quantity to 0
        response = authenticated_client.post(url, {'quantity': 0})

        assert response.status_code == status.HTTP_302_FOUND

        # Verify item was removed
        assert not CartItem.objects.filter(cart=cart, product=product).exists()

    def test_remove_product_from_cart(self, authenticated_client, user, product):
        """Test removing product from cart."""
        # Add product to cart first
        cart = Cart.objects.create(user=user)
        cart.add_product(product, 3)

        url = reverse('cart:cart_remove', kwargs={'product_id': product.id})

        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_302_FOUND

        # Verify product was removed
        assert not CartItem.objects.filter(cart=cart, product=product).exists()

    def test_clear_cart(self, authenticated_client, user):
        """Test clearing entire cart."""
        # Add multiple products to cart
        cart = Cart.objects.create(user=user)
        category = Category.objects.create(name='Test', slug='test')

        product1 = Product.objects.create(
            name='Product 1', slug='product-1', price=Decimal('10.00'),
            category=category, stock=10
        )
        product2 = Product.objects.create(
            name='Product 2', slug='product-2', price=Decimal('20.00'),
            category=category, stock=10
        )

        cart.add_product(product1, 2)
        cart.add_product(product2, 3)

        # Verify cart has items
        assert cart.total_items == 5

        url = reverse('cart:cart_clear')
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_302_FOUND

        # Verify cart is empty
        cart.refresh_from_db()
        assert cart.total_items == 0


@pytest.mark.django_db
class TestCartIntegration:
    """Integration tests for cart functionality."""

    def test_cart_persistence_across_sessions(self, authenticated_client, user, product):
        """Test that cart persists across different requests."""
        # Add product to cart
        url = reverse('cart:cart_add', kwargs={'product_id': product.id})
        authenticated_client.post(url, {'quantity': 2})

        # Verify cart contents in detail view
        detail_url = reverse('cart:cart_detail')
        response = authenticated_client.get(detail_url)

        assert response.status_code == status.HTTP_200_OK
        cart = response.context['cart']
        assert cart.total_items == 2

        # Add more of the same product
        authenticated_client.post(url, {'quantity': 3})

        # Check cart again
        response = authenticated_client.get(detail_url)
        cart = response.context['cart']
        assert cart.total_items == 5

    def test_cart_isolation_between_users(self, user):
        """Test that users have separate carts."""
        # Create two users
        User = get_user_model()
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )

        # Create products
        category = Category.objects.create(name='Test', slug='test')
        product1 = Product.objects.create(
            name='Product 1', slug='product-1', price=Decimal('10.00'),
            category=category, stock=10
        )
        product2 = Product.objects.create(
            name='Product 2', slug='product-2', price=Decimal('20.00'),
            category=category, stock=10
        )

        # Create carts for both users
        cart1 = Cart.objects.create(user=user)
        cart2 = Cart.objects.create(user=user2)

        # Add different products to each cart
        cart1.add_product(product1, 2)
        cart2.add_product(product2, 3)

        # Verify carts are isolated
        assert cart1.total_items == 2
        assert cart2.total_items == 3
        assert cart1.subtotal == Decimal('20.00')  # 2 * 10
        assert cart2.subtotal == Decimal('60.00')  # 3 * 20

    def test_cart_handles_deleted_products(self, authenticated_client, user):
        """Test cart behavior when products are deleted."""
        # Create and add product to cart
        category = Category.objects.create(name='Test', slug='test')
        product = Product.objects.create(
            name='Temp Product', slug='temp-product', price=Decimal('15.00'),
            category=category, stock=10
        )

        cart = Cart.objects.create(user=user)
        cart.add_product(product, 2)

        # Delete the product
        product_id = product.id
        product.delete()

        # Cart should still exist but calculations might be affected
        cart.refresh_from_db()
        # Note: This might cause issues with foreign key constraints
        # depending on the deletion behavior configured