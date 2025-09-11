#!/bin/bash
# Script de construcción para Render

echo "Iniciando construcción de la aplicación..."

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalación de psycopg
echo "Verificando instalación de psycopg..."
python -c "import psycopg; print('psycopg instalado correctamente')"

# Crear directorios necesarios
echo "Creando directorios necesarios..."
mkdir -p staticfiles media

# Configurar variables de entorno para producción
echo "Configurando variables de entorno..."
export DJANGO_SETTINGS_MODULE=jewerly_catalog.settings
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Ejecutar migraciones
echo "Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "Construcción completada exitosamente!"