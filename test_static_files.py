#!/usr/bin/env python
"""
Script para verificar la configuración de archivos estáticos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewerly_catalog.settings')
django.setup()

from django.conf import settings
from pathlib import Path

def test_static_configuration():
    print("=== Verificación de Archivos Estáticos ===\n")

    # Configuración actual
    print("📋 Configuración actual:")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  STATIC_URL: {settings.STATIC_URL}")
    print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"  STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    print()

    # Verificar directorios
    base_dir = Path(settings.BASE_DIR)
    static_dir = base_dir / 'static'
    staticfiles_dir = base_dir / 'staticfiles'

    print("📁 Estado de directorios:")
    print(f"  static/ existe: {static_dir.exists()}")
    if static_dir.exists():
        static_files = list(static_dir.rglob('*'))
        static_count = len([f for f in static_files if f.is_file()])
        print(f"  Archivos en static/: {static_count}")

    print(f"  staticfiles/ existe: {staticfiles_dir.exists()}")
    if staticfiles_dir.exists():
        staticfiles_files = list(staticfiles_dir.rglob('*'))
        staticfiles_count = len([f for f in staticfiles_files if f.is_file()])
        print(f"  Archivos en staticfiles/: {staticfiles_count}")
    print()

    # Recomendaciones
    print("💡 Recomendaciones:")
    if settings.DEBUG:
        print("  • Modo desarrollo: Los archivos se sirven desde static/")
        print("  • No se necesita collectstatic")
        print("  • Los cambios en CSS/JS son inmediatos")
    else:
        print("  • Modo producción: Se debe usar collectstatic")
        print("  • Los archivos se sirven desde staticfiles/")
        print("  • WhiteNoise optimiza el rendimiento")

    print()
    print("✅ Verificación completada")

if __name__ == '__main__':
    test_static_configuration()