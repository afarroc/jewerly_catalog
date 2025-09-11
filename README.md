# Jewelry Catalog

Catálogo de joyería desarrollado con Django para venta en línea.

## Características

- 🛒 Carrito de compras completo
- 💳 Integración con Stripe para pagos seguros
- 👤 Sistema de autenticación de usuarios
- 📧 Sistema de pedidos y confirmaciones por email
- 📱 **Diseño completamente responsivo** - Optimizado para móviles, tablets y desktop
- 🔒 Configuración segura para producción
- ⚡ Rendimiento optimizado con WhiteNoise
- 🎨 Interfaz moderna con animaciones suaves
- ♿ Accesibilidad mejorada con navegación por teclado
- 🌙 Soporte para modo de alto contraste
- 📊 Sistema de grid flexible de 12 columnas

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

### Opción 2: Script Automático (Recomendado)

Para desarrollo local, usa el script automatizado:
```bash
# Configuración completa de desarrollo
./dev_setup.sh

# O en Windows:
# bash dev_setup.sh
```

Este script:
- ✅ Instala dependencias
- ✅ Configura entorno de desarrollo
- ✅ Ejecuta migraciones
- ✅ Crea usuario administrador
- ✅ **NO ejecuta collectstatic** (más rápido para desarrollo)

### Archivos Estáticos en Desarrollo vs Producción

| Entorno | Archivos Estáticos | Comando | Notas |
|---------|-------------------|---------|-------|
| **Desarrollo** | Servidos desde `static/` | `python manage.py runserver` | Cambios inmediatos, sin collectstatic |
| **Producción** | Optimizados en `staticfiles/` | `python manage.py collectstatic` | WhiteNoise + compresión |

Para verificar la configuración:
```bash
python test_static_files.py
```

### Gestión de Archivos Estáticos

#### **En Desarrollo Local:**
```bash
# Los archivos se sirven automáticamente desde static/
python manage.py runserver

# Para probar collectstatic manualmente:
python manage.py collectstatic --noinput
```

#### **En Producción (Render):**
- ✅ **Collectstatic automático** en cada despliegue
- ✅ **WhiteNoise activado** para servir archivos estáticos
- ✅ **Compresión Gzip** automática
- ✅ **Cache headers** optimizados
- ✅ **Versionado de archivos** para evitar problemas de cache

#### **Configuración de WhiteNoise:**
```python
# settings.py
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Framework Bootstrap Integrado

#### Instalacion de Bootstrap

Para instalar Bootstrap en el entorno virtual:

```bash
# Activar entorno virtual
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

# Instalar Bootstrap
pip install django-bootstrap5==24.3

# Verificar instalacion
python -c "import bootstrap5; print('Bootstrap OK')"
```

#### Caracteristicas de Bootstrap

- Sistema de grid responsive de 12 columnas
- Componentes preconstruidos: cards, badges, buttons, modals
- Utilidades responsive: d-flex, text-center, mb-*, gap-*
- Breakpoints: xs, sm, md, lg, xl
- JavaScript incluido: dropdowns, modals, tooltips
- CSS compatible con estilos personalizados

#### Uso en Templates

```html
<!-- Ejemplo de grid Bootstrap -->
<div class="row">
  <div class="col-lg-3 col-md-4 col-sm-12">
    <!-- Sidebar -->
  </div>
  <div class="col-lg-9 col-md-8 col-sm-12">
    <!-- Contenido principal -->
  </div>
</div>

<!-- Ejemplo de componentes -->
<div class="card">
  <div class="card-body">
    <h5 class="card-title">Producto</h5>
    <span class="badge bg-success">En Stock</span>
  </div>
</div>
```

#### Breakpoints Responsive

| Dispositivo | Breakpoint | Columnas tipicas |
|-------------|------------|------------------|
| Movil | < 576px | 1 columna (col-12) |
| Tablet | 576px - 992px | 2 columnas (col-md-6) |
| Desktop | 992px - 1200px | 3-4 columnas (col-lg-4) |
| Desktop Grande | > 1200px | 4-5 columnas (col-xl-3) |

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

Los archivos estáticos se procesan automáticamente durante el despliegue:

#### **Collectstatic Automático:**
- ✅ **Activado en producción**: Se ejecuta cuando `DEBUG=False`
- ✅ **Script build.sh**: Maneja todo el proceso automáticamente
- ✅ **Verificación incluida**: Confirma que los archivos se procesaron correctamente

#### **Proceso de Collectstatic:**
1. **Verificación**: Confirma que existe el directorio `static/`
2. **Recopilación**: Junta todos los archivos estáticos
3. **Optimización**: WhiteNoise comprime y optimiza
4. **Almacenamiento**: Guarda en `staticfiles/` con versionado
5. **Cache**: Configura headers de cache apropiados

#### **Configuración de WhiteNoise:**
```python
# settings.py - Configuración automática
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### **Beneficios en Producción:**
- ✅ **Compresión Gzip** automática
- ✅ **Cache agresivo** para mejor rendimiento
- ✅ **Versionado de archivos** (evita problemas de cache)
- ✅ **Soporte CDN** preparado
- ✅ **Fallback inteligente** para archivos faltantes

#### **Archivos Procesados:**
- ✅ **CSS**: Comprimido y minificado
- ✅ **JavaScript**: Optimizado
- ✅ **Imágenes**: Con cache apropiado
- ✅ **Fuentes**: Optimizadas
- ✅ **Archivos de Django**: Admin, etc.

**No se requiere configuración adicional** - el sistema detecta automáticamente el entorno y aplica la configuración correcta.

## Diseño Responsive

El sitio está completamente optimizado para todos los dispositivos:

### 📱 **Breakpoints y Dispositivos Soportados**

| Dispositivo | Ancho | Características |
|-------------|-------|----------------|
| **Desktop Grande** | > 1200px | Layout completo, navegación horizontal |
| **Desktop** | 992px - 1200px | Layout adaptado, navegación horizontal |
| **Tablet** | 768px - 992px | Menú móvil, grid de 2 columnas |
| **Móvil Grande** | 576px - 768px | Menú móvil, grid de 1 columna |
| **Móvil Pequeño** | < 576px | Optimizado para touch, navegación simplificada |

### 🎯 **Características Responsive**

#### **Navegación**
- ✅ Menú hamburguesa en móviles
- ✅ Navegación por teclado completa
- ✅ Dropdowns accesibles
- ✅ Indicador de carrito visible

#### **Layout**
- ✅ Sistema de grid flexible de 12 columnas
- ✅ Contenedores adaptativos
- ✅ Espaciado responsive
- ✅ Tipografía escalable

#### **Componentes**
- ✅ Botones touch-friendly (mínimo 44px)
- ✅ Formularios optimizados para móvil
- ✅ Imágenes responsive con aspect-ratio
- ✅ Cards con hover states apropiados

#### **Accesibilidad**
- ✅ Soporte para `prefers-reduced-motion`
- ✅ Modo de alto contraste
- ✅ Navegación por teclado
- ✅ Skip links para lectores de pantalla

### 📊 **Sistema de Grid**

```css
/* Ejemplo de uso del grid responsive */
<div class="row">
  <div class="col-12 col-md-6 col-lg-4">
    <!-- Contenido responsive -->
  </div>
</div>
```

### 🎨 **Optimizaciones de Rendimiento**

- ✅ Animaciones optimizadas para móviles
- ✅ Carga diferida de imágenes
- ✅ Transiciones suaves con hardware acceleration
- ✅ Estados de carga visuales
- ✅ Optimización para touch devices

## Estructura del Proyecto

```
jewerly_catalog/
├── accounts/          # Gestión de usuarios
├── cart/             # Carrito de compras
├── home/             # Página principal
├── orders/           # Sistema de pedidos
├── products/         # Gestión de productos
├── static/           # Archivos estáticos optimizados
├── templates/        # Plantillas HTML responsive
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
