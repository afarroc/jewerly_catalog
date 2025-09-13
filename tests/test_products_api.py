import pytest
from django.urls import reverse
from rest_framework import status
from products.models import Product, Category


@pytest.mark.api
class TestProductListAPIView:
    """Test cases for ProductListAPIView."""

    def test_list_products_unauthenticated(self, api_client, product):
        """Test that unauthenticated users can list products."""
        url = reverse('products:api_product_list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert len(response.data['results']) >= 1

        # Check product data structure
        product_data = response.data['results'][0]
        assert 'id' in product_data
        assert 'name' in product_data
        assert 'price' in product_data
        assert 'available' in product_data

    def test_list_products_with_pagination(self, api_client, product):
        """Test pagination in product list."""
        url = reverse('products:api_product_list')
        response = api_client.get(url, {'page_size': 5})

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data
        assert 'count' in response.data

    def test_search_products(self, api_client, product):
        """Test product search functionality."""
        url = reverse('products:api_product_list')
        response = api_client.get(url, {'search': 'Test'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

        # Test with non-existent search term
        response = api_client.get(url, {'search': 'nonexistent'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0

    def test_filter_by_category(self, api_client, product, category):
        """Test filtering products by category."""
        url = reverse('products:api_product_list')
        response = api_client.get(url, {'category': category.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_filter_by_jewelry_type(self, api_client, product):
        """Test filtering products by jewelry type."""
        url = reverse('products:api_product_list')
        response = api_client.get(url, {'jewelry_type': 'ring'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1

    def test_filter_by_price_range(self, api_client, product):
        """Test filtering products by price range."""
        url = reverse('products:api_product_list')

        # Test minimum price
        response = api_client.get(url, {'min_price': '20.00'})
        assert response.status_code == status.HTTP_200_OK

        # Test maximum price
        response = api_client.get(url, {'max_price': '50.00'})
        assert response.status_code == status.HTTP_200_OK

        # Test price range
        response = api_client.get(url, {'min_price': '20.00', 'max_price': '50.00'})
        assert response.status_code == status.HTTP_200_OK

    def test_ordering_products(self, api_client, product):
        """Test ordering products."""
        url = reverse('products:api_product_list')

        # Test ordering by name
        response = api_client.get(url, {'ordering': 'name'})
        assert response.status_code == status.HTTP_200_OK

        # Test ordering by price
        response = api_client.get(url, {'ordering': '-price'})
        assert response.status_code == status.HTTP_200_OK

        # Test ordering by date
        response = api_client.get(url, {'ordering': '-created_at'})
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.api
class TestProductDetailAPIView:
    """Test cases for ProductDetailAPIView."""

    def test_retrieve_product(self, api_client, product):
        """Test retrieving a single product."""
        url = reverse('products:api_product_detail', kwargs={'slug': product.slug})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['name'] == product.name
        assert response.data['price'] == str(product.price)

    def test_retrieve_nonexistent_product(self, api_client):
        """Test retrieving a non-existent product."""
        url = reverse('products:api_product_detail', kwargs={'slug': 'nonexistent'})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_unavailable_product(self, api_client, unavailable_product):
        """Test that unavailable products are not accessible via API."""
        url = reverse('products:api_product_detail', kwargs={'slug': unavailable_product.slug})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.api
class TestCategoryAPIViews:
    """Test cases for Category API views."""

    def test_list_categories(self, api_client, category):
        """Test listing categories."""
        url = reverse('products:api_category_list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

        # Check category data structure
        category_data = response.data[0]
        assert 'id' in category_data
        assert 'name' in category_data
        assert 'slug' in category_data

    def test_retrieve_category(self, api_client, category):
        """Test retrieving a single category."""
        url = reverse('products:api_category_detail', kwargs={'pk': category.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == category.id
        assert response.data['name'] == category.name

    def test_retrieve_nonexistent_category(self, api_client):
        """Test retrieving a non-existent category."""
        url = reverse('products:api_category_detail', kwargs={'pk': 999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.api
class TestFeaturedProductsAPI:
    """Test cases for featured products API."""

    def test_get_featured_products(self, api_client, product):
        """Test getting featured products."""
        url = reverse('products:api_featured_products')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_featured_products_limit(self, api_client, product):
        """Test that featured products are limited to 8 items."""
        url = reverse('products:api_featured_products')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) <= 8


@pytest.mark.api
class TestProductsByCategoryAPI:
    """Test cases for products by category API."""

    def test_get_products_by_category(self, api_client, product, category):
        """Test getting products by category."""
        url = reverse('products:api_products_by_category', kwargs={'category_slug': category.slug})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) >= 1

    def test_get_products_by_nonexistent_category(self, api_client):
        """Test getting products by non-existent category."""
        url = reverse('products:api_products_by_category', kwargs={'category_slug': 'nonexistent'})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data