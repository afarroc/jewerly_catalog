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
python3 -c "import django; print('Django OK')"
python3 -c "import gunicorn; print('Gunicorn OK')"
python3 -c "import whitenoise; print('WhiteNoise OK')"

# Crear directorios necesarios
echo "Creando directorios necesarios..."
mkdir -p staticfiles media

# Configurar variables de entorno
echo "Configurando variables de entorno..."
export DJANGO_SETTINGS_MODULE=jewerly_catalog.settings
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Verificar configuración de Django
echo "Verificando configuración de Django..."
python3 manage.py check --deploy

# Ejecutar migraciones
echo "Ejecutando migraciones de base de datos..."
python3 manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python3 manage.py collectstatic --noinput --clear

# Crear usuario administrador
echo "Creando usuario administrador..."
python3 create_superuser.py

echo "Construcción completada exitosamente!"