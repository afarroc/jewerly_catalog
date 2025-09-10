# Configuración de Variables de Entorno en Render

## 📋 Lista de Variables Requeridas

Copia y pega estas variables en el dashboard de Render > Tu Servicio Web > Environment:

### Variables Obligatorias
```
SECRET_KEY=tu_clave_secreta_segura_para_produccion
DEBUG=False
ALLOWED_HOSTS=tu-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
DATABASE_URL=tu_url_de_base_de_datos_postgresql
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
STRIPE_PUBLIC_KEY=pk_live_tu_clave_publica_de_stripe
STRIPE_SECRET_KEY=sk_live_tu_clave_secreta_de_stripe
STRIPE_WEBHOOK_SECRET=whsec_tu_webhook_secret_de_stripe
```

### Variables de Configuración (Opcionales)
```
DEFAULT_CURRENCY=USD
TAX_RATE=0.08
DEFAULT_SHIPPING_COST=5.00
LOGGING_LEVEL=INFO
```

## 🔐 Pasos de Seguridad

1. **Genera una SECRET_KEY segura:**
   ```python
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

2. **Configura las variables en Render:**
   - Ve a tu Web Service
   - Selecciona "Environment"
   - Agrega cada variable con su valor correspondiente

3. **Verifica la configuración:**
   - Asegúrate de que `DEBUG=False`
   - Configura `ALLOWED_HOSTS` con tu dominio real
   - Usa credenciales de producción para Stripe

## ⚠️ Recordatorios de Seguridad

- Nunca uses las mismas credenciales en desarrollo y producción
- Mantén las claves de Stripe de producción seguras
- Cambia la SECRET_KEY si es comprometida
- No compartas estas variables en repositorios públicos

## 🚀 Verificación

Después de configurar las variables:
1. El despliegue debería funcionar sin errores 400
2. La aplicación será accesible en tu dominio de Render
3. Los pagos con Stripe funcionarán correctamente

¡Tu aplicación estará lista para producción de manera segura!