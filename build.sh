#!/bin/bash
# Script de construcción para Render

echo "Iniciando construcción de la aplicación..."

# Instalar dependencias con pip3 (más compatible en Render)
echo "Instalando dependencias..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Verificar instalación de psycopg2
echo "Verificando instalación de psycopg2..."
python3 -c "import psycopg2; print('psycopg2 instalado correctamente')"

# Crear directorios necesarios
echo "Creando directorios necesarios..."
mkdir -p staticfiles media

# Configurar variables de entorno para producción
echo "Configurando variables de entorno..."
export DJANGO_SETTINGS_MODULE=jewerly_catalog.settings
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Ejecutar migraciones
echo "Ejecutando migraciones de base de datos..."
python3 manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python3 manage.py collectstatic --noinput --clear

echo "Construcción completada exitosamente!"