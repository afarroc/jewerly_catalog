#!/bin/bash
# Script de despliegue automatizado para Render
# Uso: ./deploy.sh

set -e

echo "🚀 Iniciando proceso de despliegue a Render..."
echo "=============================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encuentra manage.py. Ejecuta este script desde la raíz del proyecto."
    exit 1
fi

# Verificar archivos necesarios
echo "📋 Verificando archivos necesarios..."
REQUIRED_FILES=("requirements.txt" "Procfile" "runtime.txt" "build.sh" ".env.example")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file encontrado"
    else
        echo "❌ $file no encontrado"
        exit 1
    fi
done

# Verificar configuración de Django
echo ""
echo "🔧 Verificando configuración de Django..."
python manage.py check --deploy

# Verificar que no hay problemas de seguridad
echo ""
echo "🔒 Verificando configuración de seguridad..."
if grep -q "DEBUG = True" jewerly_catalog/settings.py; then
    echo "⚠️  Advertencia: DEBUG está en True. Asegúrate de cambiarlo a False en producción."
fi

# Verificar archivos estáticos
echo ""
echo "📁 Verificando archivos estáticos..."
if [ -d "static" ]; then
    STATIC_COUNT=$(find static -type f | wc -l)
    echo "✅ Directorio static encontrado con $STATIC_COUNT archivos"
else
    echo "❌ Directorio static no encontrado"
    exit 1
fi

# Verificar dependencias
echo ""
echo "📦 Verificando dependencias..."
python -c "import django, gunicorn, whitenoise, pymysql, stripe; print('✅ Todas las dependencias críticas están disponibles')"

echo ""
echo "🎯 PREPARACIÓN COMPLETADA"
echo "=========================="
echo ""
echo "📋 Checklist antes del despliegue:"
echo "-----------------------------------"
echo "✅ Archivos de despliegue verificados"
echo "✅ Configuración de Django correcta"
echo "✅ Dependencias instaladas"
echo "✅ Archivos estáticos presentes"
echo ""
echo "📝 PASOS PARA DESPLEGAR EN RENDER:"
echo "==================================="
echo ""
echo "1️⃣ CREAR SERVICIOS EN RENDER:"
echo "------------------------------"
echo "   a) Ve a https://dashboard.render.com"
echo "   b) Crea una PostgreSQL Database"
echo "   c) Crea un Web Service conectado a este repositorio"
echo ""
echo "2️⃣ CONFIGURAR VARIABLES DE ENTORNO:"
echo "------------------------------------"
echo "   Agrega estas variables en Environment:"
echo ""
echo "   # Variables CRÍTICAS (requeridas):"
echo "   SECRET_KEY=django-insecure-prod-$(openssl rand -hex 32)"
echo "   DEBUG=False"
echo "   ALLOWED_HOSTS=tu-app.onrender.com"
echo "   CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com"
echo "   DATABASE_URL=[URL de tu PostgreSQL en Render]"
echo ""
echo "   # Variables RECOMENDADAS:"
echo "   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend"
echo "   EMAIL_HOST=smtp.gmail.com"
echo "   EMAIL_PORT=587"
echo "   EMAIL_USE_TLS=True"
echo "   EMAIL_HOST_USER=tu-email@gmail.com"
echo "   EMAIL_HOST_PASSWORD=tu-app-password"
echo "   DEFAULT_FROM_EMAIL=tu-email@gmail.com"
echo ""
echo "   STRIPE_PUBLIC_KEY=pk_live_..."
echo "   STRIPE_SECRET_KEY=sk_live_..."
echo "   STRIPE_WEBHOOK_SECRET=whsec_..."
echo ""
echo "3️⃣ CONFIGURACIÓN DEL WEB SERVICE:"
echo "----------------------------------"
echo "   • Runtime: Python 3"
echo "   • Build Command: ./build.sh"
echo "   • Start Command: gunicorn jewerly_catalog.wsgi:application --bind 0.0.0.0:\$PORT"
echo ""
echo "4️⃣ DESPUÉS DEL PRIMER DESPLIEGUE:"
echo "-----------------------------------"
echo "   • Ve a la Shell de tu Web Service"
echo "   • Ejecuta: python manage.py migrate"
echo "   • Ejecuta: python manage.py collectstatic (si es necesario)"
echo "   • Crea superusuario: python manage.py createsuperuser"
echo ""
echo "5️⃣ VERIFICACIÓN FINAL:"
echo "-----------------------"
echo "   • Visita tu dominio: https://tu-app.onrender.com"
echo "   • Verifica que la página carga correctamente"
echo "   • Prueba el registro de usuarios"
echo "   • Verifica que los emails se envían (si configuraste)"
echo "   • Prueba el sistema de pagos (si configuraste Stripe)"
echo ""
echo "🎉 ¡DESPLIEGUE COMPLETADO!"
echo "==========================="
echo ""
echo "💡 RECUERDA:"
echo "• Nunca subas .env con credenciales reales al repositorio"
echo "• Mantén las claves de Stripe en modo LIVE para producción"
echo "• Configura backups automáticos para la base de datos"
echo "• Monitorea los logs de Render para detectar errores"
echo ""
echo "📞 SOPORTE:"
echo "Si tienes problemas, revisa:"
echo "• Los logs de construcción en Render"
echo "• La configuración de variables de entorno"
echo "• La conexión a la base de datos PostgreSQL"
echo ""
echo "¡Tu aplicación está lista para producción! 🚀"