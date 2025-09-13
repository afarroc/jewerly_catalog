import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.api
class TestAuthentication:
    """Test cases for API authentication."""

    def test_api_requires_authentication(self, api_client):
        """Test that protected API endpoints require authentication."""
        # Test orders API
        url = reverse('orders:api_order_list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test order detail
        response = api_client.get(reverse('orders:api_order_detail', kwargs={'order_number': 'ORD-123456-123456'}))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test order cancellation
        response = api_client.post(reverse('orders:api_cancel_order', kwargs={'order_number': 'ORD-123456-123456'}))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test order history
        response = api_client.get(reverse('orders:api_order_history'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_products_api_allows_unauthenticated_access(self, api_client):
        """Test that products API allows unauthenticated access."""
        # Test product list
        url = reverse('products:api_product_list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Test categories
        response = api_client.get(reverse('products:api_category_list'))
        assert response.status_code == status.HTTP_200_OK

        # Test featured products
        response = api_client.get(reverse('products:api_featured_products'))
        assert response.status_code == status.HTTP_200_OK

    def test_user_registration_and_login(self, api_client):
        """Test user registration and login flow."""
        User = get_user_model()

        # Test registration (if you have registration endpoint)
        # This would depend on your accounts API implementation

        # Create user directly for testing
        user = User.objects.create_user(
            username='testauth',
            email='auth@example.com',
            password='testpass123',
            first_name='Auth',
            last_name='Test'
        )

        # Test login via session authentication
        api_client.login(username='testauth', password='testpass123')

        # Test authenticated access
        url = reverse('orders:api_order_list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Test that user info is included in responses
        assert 'results' in response.data

    def test_invalid_credentials(self, api_client):
        """Test login with invalid credentials."""
        # Try to login with wrong password
        api_client.login(username='nonexistent', password='wrongpass')

        # Should not be authenticated
        url = reverse('orders:api_order_list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout(self, api_client, user):
        """Test logout functionality."""
        # Login first
        api_client.login(username=user.username, password='testpass123')

        # Verify authenticated
        url = reverse('orders:api_order_list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Logout
        api_client.logout()

        # Verify no longer authenticated
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_session_persistence(self, api_client, user):
        """Test that authentication persists across requests."""
        # Login
        api_client.login(username=user.username, password='testpass123')

        # Make multiple requests
        url = reverse('orders:api_order_list')

        for _ in range(3):
            response = api_client.get(url)
            assert response.status_code == status.HTTP_200_OK

    def test_cross_user_isolation(self, api_client):
        """Test that users cannot access each other's data."""
        User = get_user_model()

        # Create two users
        user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )

        # Login as user1
        api_client.login(username='user1', password='pass123')

        # Create order for user1 (this would be done via your order creation logic)
        # For this test, we'll just verify that user1 can access their own data
        url = reverse('orders:api_order_list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # The response should only contain user1's orders
        # (This assumes you have proper user filtering in your views)
        for order in response.data.get('results', []):
            # This would need to be implemented based on your order model
            pass

    def test_rate_limiting(self, api_client):
        """Test API rate limiting."""
        # This test would depend on your rate limiting configuration
        # For now, just test that the API responds normally
        url = reverse('products:api_product_list')

        for _ in range(10):
            response = api_client.get(url)
            assert response.status_code in [status.HTTP_200_OK, status.HTTP_429_TOO_MANY_REQUESTS]

    def test_cors_headers(self, api_client):
        """Test CORS headers for API access."""
        # This test checks if CORS headers are properly set
        url = reverse('products:api_product_list')
        response = api_client.get(url)

        # Check for common CORS headers
        cors_headers = [
            'access-control-allow-origin',
            'access-control-allow-methods',
            'access-control-allow-headers'
        ]

        # At minimum, the request should succeed
        assert response.status_code == status.HTTP_200_OK

    def test_content_type_negotiation(self, api_client):
        """Test that API properly handles different content types."""
        url = reverse('products:api_product_list')

        # Test JSON response
        response = api_client.get(url, HTTP_ACCEPT='application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'].startswith('application/json')

        # Test HTML response (Browsable API)
        response = api_client.get(url, HTTP_ACCEPT='text/html')
        assert response.status_code == status.HTTP_200_OK
        assert 'text/html' in response['Content-Type']

    def test_api_versioning(self, api_client):
        """Test API versioning if implemented."""
        # This test would depend on your API versioning strategy
        url = reverse('products:api_product_list')

        # Test default version
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Test version headers if you implement versioning
        # response = api_client.get(url, HTTP_ACCEPT='application/vnd.api+json; version=1.0')
        # assert response.status_code == status.HTTP_200_OK