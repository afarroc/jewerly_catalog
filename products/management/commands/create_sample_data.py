from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from ...models import Category, Product


class Command(BaseCommand):
    help = 'Create sample data for the jewelry catalog'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data for Jewelry Catalog...')
        self.stdout.write('=' * 50)

        try:
            # Create categories
            self.stdout.write('\nCreating categories...')
            categories = self.create_categories()

            # Create products
            self.stdout.write('\nCreating products...')
            products = self.create_products(categories)

            # Create users
            self.stdout.write('\nCreating users...')
            self.create_users()

            self.stdout.write('\n' + '=' * 50)
            self.stdout.write(
                self.style.SUCCESS('Sample data created successfully!')
            )
            self.stdout.write('Summary:')
            self.stdout.write(f'   - Categories: {len(categories)}')
            self.stdout.write(f'   - Products: {len(products)}')
            self.stdout.write(f'   - Users: 2 (admin, testuser)')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating sample data: {e}')
            )

    def create_categories(self):
        """Create sample categories."""
        categories_data = [
            {
                'name': 'Anillos',
                'slug': 'anillos',
                'description': 'Anillos de diferentes estilos y materiales'
            },
            {
                'name': 'Collares',
                'slug': 'collares',
                'description': 'Collares elegantes para todas las ocasiones'
            },
            {
                'name': 'Pulseras',
                'slug': 'pulseras',
                'description': 'Pulseras modernas y clásicas'
            },
            {
                'name': 'Pendientes',
                'slug': 'pendientes',
                'description': 'Pendientes de diferentes diseños'
            }
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'[OK] Category created: {category.name}')
            else:
                self.stdout.write(f'[OK] Category exists: {category.name}')

        return categories

    def create_products(self, categories):
        """Create sample products."""
        products_data = [
            # Rings
            {
                'name': 'Anillo de Plata Clásico',
                'slug': 'anillo-plata-clasico',
                'description': 'Elegante anillo de plata 925 con diseño clásico.',
                'price': Decimal('45.00'),
                'jewelry_type': 'ring',
                'material': 'metal',
                'stock': 15,
                'available': True,
                'category': categories[0]
            },
            {
                'name': 'Anillo de Oro con Piedra',
                'slug': 'anillo-oro-piedra',
                'description': 'Anillo de oro de 18k con piedra preciosa.',
                'price': Decimal('120.00'),
                'jewelry_type': 'ring',
                'material': 'metal',
                'stock': 8,
                'available': True,
                'category': categories[0]
            },
            # Necklaces
            {
                'name': 'Collar de Plata con Colgante',
                'slug': 'collar-plata-colgante',
                'description': 'Collar delicado de plata con colgante.',
                'price': Decimal('65.00'),
                'jewelry_type': 'necklace',
                'material': 'metal',
                'stock': 12,
                'available': True,
                'category': categories[1]
            },
            # Bracelets
            {
                'name': 'Pulsera de Cuero Trenzado',
                'slug': 'pulsera-cuero-trenzado',
                'description': 'Pulsera de cuero trenzado con detalles metálicos.',
                'price': Decimal('30.00'),
                'jewelry_type': 'bracelet',
                'material': 'fabric',
                'stock': 25,
                'available': True,
                'category': categories[2]
            },
            # Earrings
            {
                'name': 'Pendientes de Plata Largos',
                'slug': 'pendientes-plata-largos',
                'description': 'Pendientes largos de plata con diseño elegante.',
                'price': Decimal('40.00'),
                'jewelry_type': 'earring',
                'material': 'metal',
                'stock': 16,
                'available': True,
                'category': categories[3]
            }
        ]

        products = []
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults=prod_data
            )
            products.append(product)
            if created:
                self.stdout.write(
                    f'[OK] Product created: {product.name} - S/. {product.price}'
                )
            else:
                self.stdout.write(f'[OK] Product exists: {product.name}')

        return products

    def create_users(self):
        """Create sample users."""
        User = get_user_model()

        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@jewelryfantasy.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )

        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('[OK] Admin user created: admin / admin123')
        else:
            self.stdout.write('[OK] Admin user exists')

        # Create test user
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )

        if created:
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write('[OK] Test user created: testuser / testpass123')
        else:
            self.stdout.write('[OK] Test user exists')