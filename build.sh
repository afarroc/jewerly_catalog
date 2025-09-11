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
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# Recolectar archivos estáticos (solo en producción)
echo "Procesando archivos estáticos..."
if [ "$DEBUG" = "False" ] || [ "$DEBUG" = "false" ] || [ -z "$DEBUG" ]; then
    echo "Modo producción: Ejecutando collectstatic con compresión..."

    # Verificar que el directorio static existe y tiene archivos
    if [ -d "static" ]; then
        STATIC_SOURCE_COUNT=$(find static -type f | wc -l)
        echo "Directorio static encontrado con $STATIC_SOURCE_COUNT archivos"

        # Mostrar archivos encontrados
        echo "Archivos estáticos encontrados:"
        find static -type f -name "*.css" | head -5 | sed 's/^/  CSS: /'
        find static -type f -name "*.js" | head -5 | sed 's/^/  JS: /'
        find static -type f -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" | head -5 | sed 's/^/  IMG: /'
    else
        echo "❌ Error: Directorio static no encontrado"
        echo "Asegúrate de que los archivos estáticos estén en el directorio 'static/'"
        exit 1
    fi

    # Crear directorio staticfiles si no existe
    mkdir -p staticfiles

    # Ejecutar collectstatic con opciones optimizadas
    echo "Ejecutando collectstatic..."
    python3 manage.py collectstatic --noinput --clear --verbosity=1

    # Verificar resultado
    if [ -d "staticfiles" ]; then
        STATIC_COUNT=$(find staticfiles -type f | wc -l)
        STATIC_SIZE=$(du -sh staticfiles 2>/dev/null | cut -f1)
        echo "✅ Collectstatic completado exitosamente"
        echo "📁 Archivos estáticos procesados: $STATIC_COUNT archivos"
        echo "📏 Tamaño total: ${STATIC_SIZE:-desconocido}"
        echo "📍 Ubicación: $(pwd)/staticfiles"

        # Verificar que se crearon los archivos principales
        if [ -f "staticfiles/static/admin/css/base.css" ]; then
            echo "✅ Archivos de Django Admin incluidos"
        fi

        if [ -d "staticfiles/static/css" ] && [ -d "staticfiles/static/js" ]; then
            echo "✅ Archivos CSS y JS del proyecto incluidos"
        fi

        # Mostrar archivos generados
        echo "Archivos generados en staticfiles:"
        find staticfiles -name "*.css" | wc -l | sed 's/^/  CSS: /'
        find staticfiles -name "*.js" | wc -l | sed 's/^/  JS: /'
        find staticfiles -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" \) | wc -l | sed 's/^/  Imágenes: /'

    else
        echo "❌ Error: Directorio staticfiles no creado"
        echo "Revisa la configuración de STATIC_ROOT en settings.py"
        exit 1
    fi
else
    echo "Modo desarrollo: Saltando collectstatic (DEBUG=True)"
    echo "💡 En desarrollo, los archivos estáticos se sirven desde $(pwd)/static"
    echo "💡 Para probar collectstatic en desarrollo: python manage.py collectstatic"
fi

# Crear usuario administrador
echo "Creando usuario administrador..."
python3 create_superuser.py

echo "Construcción completada exitosamente!"