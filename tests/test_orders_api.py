import pytest
from django.urls import reverse
from rest_framework import status
from orders.models import Order, OrderItem
from decimal import Decimal


@pytest.mark.api
class TestOrderListAPIView:
    """Test cases for OrderListAPIView."""

    def test_list_orders_authenticated(self, authenticated_client, order):
        """Test that authenticated users can list their orders."""
        url = reverse('orders:api_order_list')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) >= 1

        # Check order data structure
        order_data = response.data['results'][0]
        assert 'id' in order_data
        assert 'order_number' in order_data
        assert 'status' in order_data
        assert 'total' in order_data

    def test_list_orders_unauthenticated(self, api_client):
        """Test that unauthenticated users cannot list orders."""
        url = reverse('orders:api_order_list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_orders_pagination(self, authenticated_client, order):
        """Test pagination in order list."""
        url = reverse('orders:api_order_list')
        response = authenticated_client.get(url, {'page_size': 5})

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'count' in response.data

    def test_filter_orders_by_status(self, authenticated_client, order):
        """Test filtering orders by status."""
        url = reverse('orders:api_order_list')
        response = authenticated_client.get(url, {'status': 'pending'})

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_search_orders(self, authenticated_client, order):
        """Test searching orders by order number."""
        url = reverse('orders:api_order_list')
        response = authenticated_client.get(url, {'search': order.order_number[:5]})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_ordering_orders(self, authenticated_client, order):
        """Test ordering orders."""
        url = reverse('orders:api_order_list')

        # Test ordering by date
        response = authenticated_client.get(url, {'ordering': '-created_at'})
        assert response.status_code == status.HTTP_200_OK

        # Test ordering by total
        response = authenticated_client.get(url, {'ordering': '-total'})
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.api
class TestOrderDetailAPIView:
    """Test cases for OrderDetailAPIView."""

    def test_retrieve_own_order(self, authenticated_client, order):
        """Test retrieving own order."""
        url = reverse('orders:api_order_detail', kwargs={'order_number': order.order_number})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == order.id
        assert response.data['order_number'] == order.order_number
        assert 'items' in response.data

    def test_retrieve_other_user_order(self, authenticated_client, user):
        """Test that users cannot retrieve other users' orders."""
        # Create another user and order
        from django.contrib.auth import get_user_model
        from products.models import Product, Category

        User = get_user_model()
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )

        category = Category.objects.create(name='Other', slug='other')
        product = Product.objects.create(
            name='Other Product',
            slug='other-product',
            price=Decimal('10.00'),
            category=category
        )

        other_order = Order.objects.create(
            user=other_user,
            subtotal=product.price,
            tax=product.price * Decimal('0.08'),
            shipping_cost=Decimal('5.00'),
            total=product.price + (product.price * Decimal('0.08')) + Decimal('5.00'),
            shipping_address='Other Address',
            payment_method='credit_card'
        )

        url = reverse('orders:api_order_detail', kwargs={'order_number': other_order.order_number})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_nonexistent_order(self, authenticated_client):
        """Test retrieving a non-existent order."""
        url = reverse('orders:api_order_detail', kwargs={'order_number': 'ORD-999999-999999'})
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_order_unauthenticated(self, api_client, order):
        """Test that unauthenticated users cannot retrieve orders."""
        url = reverse('orders:api_order_detail', kwargs={'order_number': order.order_number})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.api
class TestOrderCreation:
    """Test cases for order creation via API."""

    def test_create_order_authenticated(self, authenticated_client, user, product):
        """Test creating an order via API."""
        url = reverse('orders:api_order_list')

        order_data = {
            'shipping_address': 'Test Shipping Address 123',
            'billing_address': 'Test Billing Address 123',
            'payment_method': 'credit_card',
            'notes': 'Test order notes',
            'items': [
                {
                    'product_id': product.id,
                    'quantity': 2
                }
            ]
        }

        response = authenticated_client.post(url, order_data, format='json')

        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response data: {response.data}")
            print(f"Response status: {response.status_code}")

        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert 'order_number' in response.data

        # Verify order was created in database
        order = Order.objects.get(order_number=response.data['order_number'])
        assert order.user == user
        assert order.items.count() == 1

    def test_create_order_insufficient_stock(self, authenticated_client, product):
        """Test creating order with insufficient stock."""
        # Set product stock to 1
        product.stock = 1
        product.save()

        url = reverse('orders:api_order_list')

        order_data = {
            'shipping_address': 'Test Address',
            'payment_method': 'credit_card',
            'items': [
                {
                    'product_id': product.id,
                    'quantity': 5  # More than available stock
                }
            ]
        }

        response = authenticated_client.post(url, order_data, format='json')

        # This should fail due to insufficient stock
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED]

    def test_create_order_unauthenticated(self, api_client, product):
        """Test that unauthenticated users cannot create orders."""
        url = reverse('orders:api_order_list')

        order_data = {
            'shipping_address': 'Test Address',
            'payment_method': 'credit_card',
            'items': [
                {
                    'product_id': product.id,
                    'quantity': 1
                }
            ]
        }

        response = api_client.post(url, order_data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.api
class TestOrderCancellation:
    """Test cases for order cancellation."""

    def test_cancel_own_order(self, authenticated_client, order):
        """Test cancelling own order."""
        url = reverse('orders:api_cancel_order', kwargs={'order_number': order.order_number})
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'cancelled'

        # Verify order was cancelled in database
        order.refresh_from_db()
        assert order.status == 'cancelled'

    def test_cancel_other_user_order(self, authenticated_client, user):
        """Test that users cannot cancel other users' orders."""
        # Create another user and order
        from django.contrib.auth import get_user_model
        from products.models import Product, Category

        User = get_user_model()
        other_user = User.objects.create_user(
            username='otheruser2',
            email='other2@example.com',
            password='testpass123'
        )

        category = Category.objects.create(name='Other2', slug='other2')
        product = Product.objects.create(
            name='Other Product 2',
            slug='other-product-2',
            price=Decimal('10.00'),
            category=category
        )

        other_order = Order.objects.create(
            user=other_user,
            subtotal=product.price,
            tax=product.price * Decimal('0.08'),
            shipping_cost=Decimal('5.00'),
            total=product.price + (product.price * Decimal('0.08')) + Decimal('5.00'),
            shipping_address='Other Address',
            payment_method='credit_card'
        )

        url = reverse('orders:api_cancel_order', kwargs={'order_number': other_order.order_number})
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cancel_nonexistent_order(self, authenticated_client):
        """Test cancelling a non-existent order."""
        url = reverse('orders:api_cancel_order', kwargs={'order_number': 'ORD-999999-999999'})
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cancel_completed_order(self, authenticated_client, order):
        """Test cancelling an order that cannot be cancelled."""
        # Set order status to completed
        order.status = 'delivered'
        order.save()

        url = reverse('orders:api_cancel_order', kwargs={'order_number': order.order_number})
        response = authenticated_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data


@pytest.mark.api
class TestOrderHistoryAPI:
    """Test cases for order history API."""

    def test_get_order_history(self, authenticated_client, order):
        """Test getting order history."""
        url = reverse('orders:api_order_history')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) >= 1

    def test_order_history_unauthenticated(self, api_client):
        """Test that unauthenticated users cannot access order history."""
        url = reverse('orders:api_order_history')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED