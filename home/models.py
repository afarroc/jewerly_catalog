from django.db import models
from django.core.exceptions import ValidationError
import os


def validate_image_extension(value):
    """Validar que la imagen tenga una extensión permitida"""
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError('Solo se permiten archivos de imagen: JPG, PNG, WebP')


class Banner(models.Model):
    """
    Modelo para banners de la página principal
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Título del Banner",
        help_text="Título principal que se mostrará en el banner"
    )

    subtitle = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Subtítulo",
        help_text="Subtítulo opcional para el banner"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Descripción detallada del banner"
    )

    # Campo para la imagen estática (no usa FileField, solo referencia)
    image_filename = models.CharField(
        max_length=255,
        verbose_name="Nombre del Archivo de Imagen",
        help_text="Nombre del archivo de imagen en static/images/banners/ (ej: banner1.jpg)",
        unique=True
    )

    # Campos de control
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Si está marcado, el banner se mostrará en la página principal"
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición (menor número = mayor prioridad)"
    )

    # Campos de enlace opcional
    button_text = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Texto del Botón",
        help_text="Texto que aparecerá en el botón de acción"
    )

    button_url = models.URLField(
        blank=True,
        verbose_name="URL del Botón",
        help_text="URL a la que redirigirá el botón (opcional)"
    )

    # Campos de fecha
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Modificación")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_image_url(self):
        """Obtener la URL completa de la imagen"""
        return f"/static/images/banners/{self.image_filename}"

    def clean(self):
        """Validaciones personalizadas"""
        if self.button_text and not self.button_url:
            raise ValidationError("Si especifica texto del botón, debe proporcionar una URL")
        if not self.button_text and self.button_url:
            raise ValidationError("Si especifica una URL del botón, debe proporcionar texto del botón")

    @property
    def has_button(self):
        """Verificar si el banner tiene botón configurado"""
        return bool(self.button_text and self.button_url)
