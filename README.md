# Jewelry Catalog

Catálogo de joyería desarrollado con Django para venta en línea.

## Características

- 🛒 Carrito de compras
- 💳 Integración con Stripe para pagos
- 👤 Sistema de autenticación de usuarios
- 📧 Sistema de pedidos y confirmaciones
- 📱 Diseño responsivo
- 🔒 Configuración segura para producción

## Tecnologías

- **Backend**: Django 5.2.3
- **Base de datos**: PostgreSQL (producción) / MySQL (desarrollo local)
- **Pagos**: Stripe
- **Despliegue**: Render
- **Archivos estáticos**: WhiteNoise

## Instalación Local

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd jewerly_catalog
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus configuraciones locales
# Asegúrate de que las credenciales de MySQL estén configuradas
```

5. Asegúrate de que MySQL esté ejecutándose localmente con:
   - **Host**: 127.0.0.1
   - **Puerto**: 3306
   - **Base de datos**: projects
   - **Usuario**: admin
   - **Contraseña**: Peru+123

6. Ejecuta las migraciones:
```bash
python manage.py migrate
```

6. Crea un superusuario:
```bash
python manage.py createsuperuser
```

7. Ejecuta el servidor:
```bash
python manage.py runserver
```

## Despliegue en Render

### 1. Preparación del Repositorio

Asegúrate de que los siguientes archivos estén en tu repositorio:
- `requirements.txt` - Dependencias de Python
- `Procfile` - Comando para ejecutar la aplicación
- `runtime.txt` - Versión de Python
- `.env.example` - Variables de entorno de ejemplo

### 2. Crear Servicio Web en Render

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Crea un nuevo **Web Service**
3. Conecta tu repositorio de GitHub/GitLab
4. Configura el servicio:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: Se configura automáticamente desde Procfile

### 3. Configurar Base de Datos PostgreSQL

1. Crea una nueva **PostgreSQL Database** en Render
2. Copia la **Internal Database URL**
3. En las variables de entorno del Web Service, agrega:
   - `DATABASE_URL`: URL de la base de datos PostgreSQL

### 4. Configurar Variables de Entorno

En el dashboard de Render, configura estas variables de entorno (copia los valores del archivo `.env.production`):

#### Requeridas:
- `SECRET_KEY`: `django-insecure-production-key-change-this-in-render-dashboard`
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: Tu dominio en Render (ej: `tu-app.onrender.com`)
- `CSRF_TRUSTED_ORIGINS`: `https://tu-app.onrender.com`
- `DATABASE_URL`: `postgresql://admin:wSPH2XQ1sB6DGlTwVEn84XQVYtFxTRPO@dpg-d30vl97fte5s73ftlnlg-a/projects_8gq2`

#### Opcionales (para funcionalidades completas):
- `EMAIL_BACKEND`: `django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST`: `smtp.gmail.com`
- `EMAIL_PORT`: `587`
- `EMAIL_USE_TLS`: `True`
- `EMAIL_HOST_USER`: Tu email de Gmail
- `EMAIL_HOST_PASSWORD`: Tu app password de Gmail
- `DEFAULT_FROM_EMAIL`: `Fantasy Jewelry <noreply@fantasyjewelry.com>`
- `STRIPE_PUBLIC_KEY`: Tu clave pública de Stripe (live)
- `STRIPE_SECRET_KEY`: Tu clave secreta de Stripe (live)
- `STRIPE_WEBHOOK_SECRET`: Tu webhook secret de Stripe
- `DEFAULT_CURRENCY`: `USD`
- `TAX_RATE`: `0.08`
- `DEFAULT_SHIPPING_COST`: `5.00`

### 5. Migraciones de Base de Datos

Después del primer despliegue, ejecuta las migraciones:
```bash
# En la shell de Render o usando el comando personalizado
python manage.py migrate
```

### 6. Seguridad Importante

⚠️ **IMPORTANTE**: Nunca subas el archivo `.env.production` al repositorio. Este archivo contiene credenciales sensibles y está protegido por `.gitignore`.

Para configurar las variables de entorno en producción:
1. Copia los valores del archivo `.env.production` local
2. Pégalos en el dashboard de Render en "Environment"
3. **Cambia la SECRET_KEY** por una clave segura generada específicamente para producción
4. Configura las claves de Stripe y credenciales de email según corresponda

### 6. Archivos Estáticos

Los archivos estáticos se sirven automáticamente con WhiteNoise. No se requiere configuración adicional.

## Estructura del Proyecto

```
jewerly_catalog/
├── accounts/          # Gestión de usuarios
├── cart/             # Carrito de compras
├── home/             # Página principal
├── orders/           # Sistema de pedidos
├── products/         # Gestión de productos
├── static/           # Archivos estáticos
├── templates/        # Plantillas HTML
├── jewerly_catalog/  # Configuración principal
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── README.md
```

## Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar pruebas
python manage.py test
```

## Configuración de Stripe

1. Crea una cuenta en [Stripe](https://stripe.com)
2. Obtén tus claves API (Publishable key y Secret key)
3. Configura los webhooks para confirmar pagos
4. Agrega las claves a las variables de entorno

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
