# Configuración de Variables de Entorno en Render

## 📋 Lista de Variables Requeridas

Copia y pega estas variables en el dashboard de Render > Tu Servicio Web > Environment:

### Variables Obligatorias
```
SECRET_KEY=django-insecure-production-key-change-this-in-render-dashboard
DEBUG=False
ALLOWED_HOSTS=tu-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
DATABASE_URL=postgresql://admin:wSPH2XQ1sB6DGlTwVEn84XQVYtFxTRPO@dpg-d30vl97fte5s73ftlnlg-a/projects_8gq2
```

### Variables para Email (Opcionales)
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=Fantasy Jewelry <noreply@fantasyjewelry.com>
```

### Variables para Stripe (Opcionales)
```
STRIPE_PUBLIC_KEY=pk_live_tu_clave_publica
STRIPE_SECRET_KEY=sk_live_tu_clave_secreta
STRIPE_WEBHOOK_SECRET=whsec_tu_webhook_secret
```

### Variables de Configuración (Opcionales)
```
DEFAULT_CURRENCY=USD
TAX_RATE=0.08
DEFAULT_SHIPPING_COST=5.00
LOGGING_LEVEL=INFO
```

## 🔐 Pasos de Seguridad

1. **Cambia la SECRET_KEY** por una clave segura generada específicamente para producción
2. **Configura las claves de Stripe** con las credenciales de producción (live)
3. **Configura el email** con credenciales válidas para envío de correos
4. **Verifica ALLOWED_HOSTS** con tu dominio real en Render

## ⚠️ Recordatorios de Seguridad

- Nunca subas `.env.production` al repositorio
- Las variables sensibles están protegidas por `.gitignore`
- Usa siempre claves de producción (live) para Stripe
- Cambia la SECRET_KEY por una única para producción

## 🚀 Verificación

Después de configurar las variables:
1. Despliega la aplicación
2. Verifica que la base de datos PostgreSQL se conecte correctamente
3. Prueba el envío de emails
4. Verifica que los pagos con Stripe funcionen

¡Tu aplicación estará lista para producción!