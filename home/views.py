# home/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from products.models import Product
from .models import Banner, SocialMedia
import logging

logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    """Class-based view for the home page."""
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Obtener banners activos ordenados por prioridad
            active_banners = Banner.objects.filter(is_active=True).order_by('order', '-created_at')

            # Obtener redes sociales activas ordenadas por prioridad
            active_social_media = SocialMedia.objects.filter(is_active=True).order_by('order', 'platform')

            # Obtener productos destacados
            featured_products = Product.objects.filter(available=True).order_by('-created_at')[:8]

            logger.debug(f"Mostrando {len(active_banners)} banners, {len(active_social_media)} redes sociales y {len(featured_products)} productos")

        except Exception as e:
            active_banners = []
            active_social_media = []
            featured_products = []
            logger.error(f"Error al obtener datos para la página de inicio: {str(e)}")

        context.update({
            'title': 'Catálogo de Joyería Fantasía',
            'welcome_message': '¡Bienvenido a nuestra Colección de Joyería Fantasía!',
            'banners': active_banners,
            'social_media': active_social_media,
            'featured_products': featured_products,
        })

        return context


def index(request):
    """Legacy function-based view for backward compatibility."""
    view = IndexView.as_view()
    return view(request)