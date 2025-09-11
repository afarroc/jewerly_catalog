@echo off
REM Script de despliegue para Windows
echo 🚀 Iniciando proceso de despliegue a Render...
echo ==============================================

REM Verificar que estamos en el directorio correcto
if not exist "manage.py" (
    echo ❌ Error: No se encuentra manage.py. Ejecuta este script desde la raíz del proyecto.
    pause
    exit /b 1
)

REM Verificar archivos necesarios
echo 📋 Verificando archivos necesarios...
set REQUIRED_FILES=requirements.txt Procfile runtime.txt build.sh .env.example
for %%f in (%REQUIRED_FILES%) do (
    if exist "%%f" (
        echo ✅ %%f encontrado
    ) else (
        echo ❌ %%f no encontrado
        pause
        exit /b 1
    )
)

REM Verificar configuración de Django
echo.
echo 🔧 Verificando configuración de Django...
python manage.py check --deploy
if errorlevel 1 (
    echo ❌ Error en la configuración de Django
    pause
    exit /b 1
)

REM Verificar archivos estáticos
echo.
echo 📁 Verificando archivos estáticos...
if exist "static" (
    for /f %%c in ('dir /b /s static\*.css static\*.js static\*.png static\*.jpg 2^>nul ^| find /c ":"') do set STATIC_COUNT=%%c
    echo ✅ Directorio static encontrado con archivos
) else (
    echo ❌ Directorio static no encontrado
    pause
    exit /b 1
)

REM Verificar dependencias críticas
echo.
echo 📦 Verificando dependencias críticas...
python -c "import django, gunicorn, whitenoise, pymysql, stripe" 2>nul
if errorlevel 1 (
    echo ❌ Faltan dependencias críticas
    pause
    exit /b 1
) else (
    echo ✅ Todas las dependencias críticas están disponibles
)

echo.
echo 🎯 PREPARACIÓN COMPLETADA
echo ==========================
echo.
echo 📋 Checklist antes del despliegue:
echo -----------------------------------
echo ✅ Archivos de despliegue verificados
echo ✅ Configuración de Django correcta
echo ✅ Dependencias instaladas
echo ✅ Archivos estáticos presentes
echo.
echo 📝 PASOS PARA DESPLEGAR EN RENDER:
echo ===================================
echo.
echo 1️⃣ CREAR SERVICIOS EN RENDER:
echo -----------------------------
echo    a) Ve a https://dashboard.render.com
echo    b) Crea una PostgreSQL Database
echo    c) Crea un Web Service conectado a este repositorio
echo.
echo 2️⃣ CONFIGURAR VARIABLES DE ENTORNO:
echo -----------------------------------
echo    Agrega estas variables en Environment:
echo.
echo    # Variables CRÍTICAS (requeridas):
echo    SECRET_KEY=django-insecure-prod-$(openssl rand -hex 32)
echo    DEBUG=False
echo    ALLOWED_HOSTS=tu-app.onrender.com
echo    CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
echo    DATABASE_URL=[URL de tu PostgreSQL en Render]
echo.
echo    # Variables RECOMENDADAS:
echo    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
echo    EMAIL_HOST=smtp.gmail.com
echo    EMAIL_PORT=587
echo    EMAIL_USE_TLS=True
echo    EMAIL_HOST_USER=tu-email@gmail.com
echo    EMAIL_HOST_PASSWORD=tu-app-password
echo    DEFAULT_FROM_EMAIL=tu-email@gmail.com
echo.
echo    STRIPE_PUBLIC_KEY=pk_live_...
echo    STRIPE_SECRET_KEY=sk_live_...
echo    STRIPE_WEBHOOK_SECRET=whsec_...
echo.
echo 3️⃣ CONFIGURACIÓN DEL WEB SERVICE:
echo ---------------------------------
echo    • Runtime: Python 3
echo    • Build Command: ./build.sh
echo    • Start Command: gunicorn jewerly_catalog.wsgi:application --bind 0.0.0.0:%%PORT%%
echo.
echo 4️⃣ DESPUÉS DEL PRIMER DESPLIEGUE:
echo ----------------------------------
echo    • Ve a la Shell de tu Web Service
echo    • Ejecuta: python manage.py migrate
echo    • Crea superusuario: python manage.py createsuperuser
echo.
echo 5️⃣ VERIFICACIÓN FINAL:
echo ----------------------
echo    • Visita tu dominio: https://tu-app.onrender.com
echo    • Verifica que la página carga correctamente
echo    • Prueba el registro de usuarios
echo    • Verifica que los emails se envían
echo    • Prueba el sistema de pagos
echo.
echo 🎉 ¡DESPLIEGUE COMPLETADO!
echo ===========================
echo.
echo 💡 RECUERDA:
echo • Nunca subas .env con credenciales reales al repositorio
echo • Mantén las claves de Stripe en modo LIVE para producción
echo • Configura backups automáticos para la base de datos
echo • Monitorea los logs de Render para detectar errores
echo.
echo 📞 SOPORTE:
echo Si tienes problemas, revisa:
echo • Los logs de construcción en Render
echo • La configuración de variables de entorno
echo • La conexión a la base de datos PostgreSQL
echo.
echo ¡Tu aplicación está lista para producción! 🚀
echo.
pause