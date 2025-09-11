from django.core.management.base import BaseCommand
from home.models import SocialMedia

class Command(BaseCommand):
    help = 'Crear datos de ejemplo de redes sociales'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Eliminar todas las redes sociales existentes antes de crear las nuevas',
        )

    def handle(self, *args, **options):
        if options['reset']:
            SocialMedia.objects.all().delete()
            self.stdout.write(
                self.style.WARNING('Eliminadas todas las redes sociales existentes')
            )

        social_media_data = [
            {
                'name': 'Facebook',
                'platform': 'facebook',
                'url': 'https://www.facebook.com/joyeriafantasia',
                'is_active': True,
                'order': 1,
                'followers_count': 12500,
            },
            {
                'name': 'Instagram',
                'platform': 'instagram',
                'url': 'https://www.instagram.com/joyeriafantasia',
                'is_active': True,
                'order': 2,
                'followers_count': 8900,
            },
            {
                'name': 'Pinterest',
                'platform': 'pinterest',
                'url': 'https://www.pinterest.com/joyeriafantasia',
                'is_active': True,
                'order': 3,
                'followers_count': 5600,
            },
            {
                'name': 'Twitter',
                'platform': 'twitter',
                'url': 'https://www.twitter.com/joyeriafantasia',
                'is_active': True,
                'order': 4,
                'followers_count': 3200,
            },
        ]

        created_count = 0
        for data in social_media_data:
            social, created = SocialMedia.objects.get_or_create(
                platform=data['platform'],
                defaults=data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Creada red social: {social.name} ({social.platform})')
                )
                created_count += 1
            else:
                self.stdout.write(
                    f'Ya existe: {social.name} ({social.platform})'
                )

        total_active = SocialMedia.objects.filter(is_active=True).count()
        self.stdout.write(
            self.style.SUCCESS(
                f'\nResumen: {created_count} redes sociales creadas, '
                f'{total_active} redes sociales activas en total'
            )
        )