#!/bin/bash
# Script de construcción para Render

set -e  # Salir si hay algún error

echo "Iniciando construcción de la aplicación..."

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalación de dependencias críticas
echo "Verificando dependencias críticas..."
python -c "import django; print('Django OK')"
python -c "import gunicorn; print('Gunicorn OK')"
python -c "import whitenoise; print('WhiteNoise OK')"

# Crear directorios necesarios
echo "Creando directorios necesarios..."
mkdir -p staticfiles media

# Configurar variables de entorno
echo "Configurando variables de entorno..."
export DJANGO_SETTINGS_MODULE=jewerly_catalog.settings
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Verificar configuración de Django
echo "Verificando configuración de Django..."
python manage.py check --deploy

# Ejecutar migraciones
echo "Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Construcción completada exitosamente!"