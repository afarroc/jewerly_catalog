from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import AnonymousUser
from .views import register, login_view, logout_view, profile, profile_update
from .forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm
from .models import User

class AccountsURLsTestCase(TestCase):
    """Test URL patterns and resolution."""

    def test_register_url_resolves(self):
        """Test that register URL resolves to correct view."""
        url = reverse('accounts:register')
        self.assertEqual(url, '/accounts/register/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, register)

    def test_login_url_resolves(self):
        """Test that login URL resolves to correct view."""
        url = reverse('accounts:login')
        self.assertEqual(url, '/accounts/login/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, login_view)

    def test_logout_url_resolves(self):
        """Test that logout URL resolves to correct view."""
        url = reverse('accounts:logout')
        self.assertEqual(url, '/accounts/logout/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, logout_view)

    def test_profile_url_resolves(self):
        """Test that profile URL resolves to correct view."""
        url = reverse('accounts:profile')
        self.assertEqual(url, '/accounts/profile/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, profile)

    def test_profile_update_url_resolves(self):
        """Test that profile update URL resolves to correct view."""
        url = reverse('accounts:profile_update')
        self.assertEqual(url, '/accounts/profile/update/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, profile_update)

    def test_password_reset_urls_resolve(self):
        """Test that password reset URLs resolve correctly."""
        # Test password reset
        url = reverse('accounts:password_reset')
        self.assertEqual(url, '/accounts/password-reset/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class.__name__, 'PasswordResetView')

        # Test password reset done
        url = reverse('accounts:password_reset_done')
        self.assertEqual(url, '/accounts/password-reset/done/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class.__name__, 'PasswordResetDoneView')

        # Test password reset confirm
        url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': 'test', 'token': 'test'})
        self.assertEqual(url, '/accounts/password-reset-confirm/test/test/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class.__name__, 'PasswordResetConfirmView')

        # Test password reset complete
        url = reverse('accounts:password_reset_complete')
        self.assertEqual(url, '/accounts/password-reset-complete/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class.__name__, 'PasswordResetCompleteView')


class AccountsViewsTestCase(TestCase):
    """Test view functions."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'remember_me': False,
        }
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            phone_number='1234567890'
        )

    def test_register_view_get(self):
        """Test GET request to register view."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIsInstance(response.context['form'], UserRegisterForm)

    def test_register_view_post_success(self):
        """Test successful POST request to register view."""
        # Use different data to avoid conflict with setUp user
        new_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'phone_number': '1234567890',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(reverse('accounts:register'), new_user_data, follow=True)
        self.assertRedirects(response, reverse('home:index'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Account created for newuser!')

    def test_register_view_post_duplicate_email(self):
        """Test POST request with duplicate email."""
        # Create first user
        User.objects.create_user(
            username='existinguser',
            email='test@example.com',
            password='testpass123'
        )

        response = self.client.post(reverse('accounts:register'), self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertContains(response, 'This email is already in use.')

    def test_register_view_post_invalid_form(self):
        """Test POST request with invalid form data."""
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'differentpassword'
        response = self.client.post(reverse('accounts:register'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertFalse(response.context['form'].is_valid())

    def test_login_view_get(self):
        """Test GET request to login view."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], UserLoginForm)

    def test_login_view_authenticated_redirect(self):
        """Test that authenticated users are redirected."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:login'))
        self.assertRedirects(response, reverse('home:index'))

    def test_login_view_post_success(self):
        """Test successful login."""
        response = self.client.post(reverse('accounts:login'), self.login_data, follow=True)
        self.assertRedirects(response, reverse('home:index'))

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Welcome back, testuser!')

    def test_login_view_post_success_with_next(self):
        """Test successful login with next parameter."""
        url = reverse('accounts:login') + '?next=' + reverse('accounts:profile')
        response = self.client.post(url, self.login_data, follow=True)
        self.assertRedirects(response, reverse('accounts:profile'))

    def test_login_view_post_invalid_credentials(self):
        """Test login with invalid credentials."""
        invalid_data = self.login_data.copy()
        invalid_data['password'] = 'wrongpassword'
        response = self.client.post(reverse('accounts:login'), invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertFalse(response.context['form'].is_valid())

    def test_logout_view(self):
        """Test logout view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertRedirects(response, reverse('home:index'))

        # Check logout message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have been logged out.')

    def test_profile_view_requires_login(self):
        """Test that profile view requires login."""
        response = self.client.get(reverse('accounts:profile'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:profile')}")

    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.context['user'], self.user)

    def test_profile_update_view_requires_login(self):
        """Test that profile update view requires login."""
        response = self.client.get(reverse('accounts:profile_update'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:profile_update')}")

    def test_profile_update_view_get(self):
        """Test GET request to profile update view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_update.html')
        self.assertIsInstance(response.context['form'], ProfileUpdateForm)

    def test_profile_update_view_post_success(self):
        """Test successful profile update."""
        self.client.login(username='testuser', password='testpass123')
        update_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '0987654321',
            'address': '123 Main St',
        }
        response = self.client.post(reverse('accounts:profile_update'), update_data, follow=True)
        self.assertRedirects(response, reverse('accounts:profile'))

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your profile has been updated!')

        # Check that user was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'john@example.com')

    def test_profile_update_view_post_invalid_email(self):
        """Test profile update with duplicate email."""
        # Create another user
        User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )

        self.client.login(username='testuser', password='testpass123')
        update_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'other@example.com',  # Duplicate email
            'phone_number': '0987654321',
            'address': '123 Main St',
        }
        response = self.client.post(reverse('accounts:profile_update'), update_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_update.html')
        self.assertFalse(response.context['form'].is_valid())


class AccountsFormsTestCase(TestCase):
    """Test form classes."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_register_form_valid(self):
        """Test valid UserRegisterForm."""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone_number': '1234567890',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_register_form_duplicate_email(self):
        """Test UserRegisterForm with duplicate email."""
        form_data = {
            'username': 'newuser',
            'email': 'test@example.com',  # Duplicate email
            'phone_number': '1234567890',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'This email is already in use.')

    def test_user_register_form_invalid_passwords(self):
        """Test UserRegisterForm with mismatched passwords."""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone_number': '1234567890',
            'password1': 'testpass123',
            'password2': 'differentpass',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_login_form_valid(self):
        """Test valid UserLoginForm."""
        form_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'remember_me': True,
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_update_form_valid(self):
        """Test valid ProfileUpdateForm."""
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '0987654321',
            'address': '123 Main St',
        }
        form = ProfileUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_profile_update_form_duplicate_email(self):
        """Test ProfileUpdateForm with duplicate email."""
        # Create another user
        User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )

        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'other@example.com',  # Duplicate email
            'phone_number': '0987654321',
            'address': '123 Main St',
        }
        form = ProfileUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class AccountsModelsTestCase(TestCase):
    """Test model classes."""

    def test_user_creation(self):
        """Test user creation."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            phone_number='1234567890',
            address='123 Main St'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.address, '123 Main St')
        self.assertTrue(user.is_customer)
        self.assertEqual(str(user), 'testuser')

    def test_user_str_method(self):
        """Test User __str__ method."""
        user = User(username='testuser')
        self.assertEqual(str(user), 'testuser')
