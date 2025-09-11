# home/context_processors.py
from .models import SocialMedia
import logging

logger = logging.getLogger(__name__)

def social_media(request):
    """Make social media links available to all templates."""
    try:
        # Obtener redes sociales activas ordenadas por prioridad
        active_social_media = SocialMedia.objects.filter(is_active=True).order_by('order', 'platform')
        return {
            'social_media': active_social_media
        }
    except Exception as e:
        logger.error(f"Error al obtener redes sociales en context processor: {str(e)}")
        return {
            'social_media': []
        }