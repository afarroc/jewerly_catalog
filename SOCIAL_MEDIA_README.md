# Sistema de Redes Sociales - Catálogo de Joyería Fantasía

## 📋 Descripción
El sistema de redes sociales permite gestionar y mostrar enlaces a las redes sociales de la tienda en todo el sitio web. Está completamente integrado con el administrador de Django y disponible en todas las plantillas.

## 🚀 Características

### ✅ Funcionalidades Implementadas
- **Modelo SocialMedia** completo con validaciones
- **Administrador de Django** con interfaz intuitiva
- **Context Processor** global para todas las plantillas
- **Footer moderno** con diseño responsivo
- **Iconos automáticos** basados en la plataforma
- **Orden personalizado** de redes sociales
- **Estados activo/inactivo** para control
- **Contador de seguidores** opcional

### 🎨 Diseño del Footer
- **Efectos de vidrio** con backdrop-filter
- **Animaciones suaves** y transiciones
- **Responsive design** para móviles
- **Newsletter integrado**
- **Información de contacto**
- **Enlaces organizados** por categorías

## 🛠️ Instalación y Configuración

### 1. Modelo y Migraciones
El modelo `SocialMedia` ya está creado y las migraciones aplicadas:
```bash
# Verificar migraciones
python manage.py showmigrations home

# Aplicar migraciones si es necesario
python manage.py migrate
```

### 2. Context Processor
Ya está registrado en `settings.py`:
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... otros context processors
                'home.context_processors.social_media',
            ],
        },
    },
]
```

## 📊 Uso del Administrador

### Acceder al Administrador
1. Inicia sesión en `/admin/`
2. Ve a **Home > Redes sociales**
3. Gestiona tus redes sociales

### Campos del Modelo
- **Nombre**: Nombre descriptivo de la red social
- **Plataforma**: Facebook, Instagram, Twitter, etc.
- **URL**: Enlace completo al perfil
- **Activa**: Mostrar/ocultar en el sitio
- **Orden**: Prioridad de aparición
- **Seguidores**: Número aproximado (opcional)

### Iconos Automáticos
Los iconos se asignan automáticamente según la plataforma:
- Facebook → `fab fa-facebook-f`
- Instagram → `fab fa-instagram`
- Twitter → `fab fa-twitter`
- YouTube → `fab fa-youtube`
- Pinterest → `fab fa-pinterest-p`
- LinkedIn → `fab fa-linkedin-in`
- WhatsApp → `fab fa-whatsapp`
- Telegram → `fab fa-telegram-plane`

## 🎯 Crear Datos de Ejemplo

### Comando de Management
```bash
# Crear redes sociales de ejemplo
python manage.py create_social_media

# Resetear y crear nuevas
python manage.py create_social_media --reset
```

### Datos de Ejemplo Creados
- **Facebook**: https://www.facebook.com/joyeriafantasia (12.5K seguidores)
- **Instagram**: https://www.instagram.com/joyeriafantasia (8.9K seguidores)
- **Pinterest**: https://www.pinterest.com/joyeriafantasia (5.6K seguidores)
- **Twitter**: https://www.twitter.com/joyeriafantasia (3.2K seguidores)

## 🎨 Personalización del Footer

### Variables CSS Personalizables
```css
/* Colores del footer */
--primary-color: #6a4c93;
--accent-color: #f8c537;

/* Espaciado */
--spacing-lg: 1.5rem;
--spacing-xl: 2rem;

/* Bordes y sombras */
--border-radius-lg: 12px;
--box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
```

### Modificar la Estructura
El footer está en `home/templates/home/base.html` y se puede personalizar:
- Cambiar el orden de las columnas
- Modificar los enlaces de navegación
- Personalizar la información de contacto
- Ajustar el formulario de newsletter

## 📱 Responsive Design

### Breakpoints
- **Desktop**: > 992px - Layout de 2 columnas
- **Tablet**: 768px - 992px - Columnas apiladas
- **Mobile**: < 768px - Diseño compacto

### Características Móviles
- **Menú colapsable** para redes sociales
- **Iconos sin texto** en pantallas pequeñas
- **Newsletter simplificado**
- **Información de contacto** optimizada

## 🔧 Uso en Plantillas

### Variable Disponible
En todas las plantillas tienes acceso a `{{ social_media }}`:
```html
{% for social in social_media %}
    <a href="{{ social.url }}" title="{{ social.name }}">
        <i class="{{ social.platform_icon }}"></i>
        {{ social.name }}
    </a>
{% endfor %}
```

### Propiedades del Modelo
- `social.name` - Nombre de la red social
- `social.platform` - Plataforma (facebook, instagram, etc.)
- `social.url` - URL del perfil
- `social.platform_icon` - Clase CSS del icono
- `social.display_followers` - Seguidores formateados
- `social.is_active` - Estado activo/inactivo

## 🎨 Estilos CSS

### Clases Principales
- `.footer-modern` - Contenedor principal
- `.footer-content` - Contenido del footer
- `.footer-main` - Layout principal
- `.footer-brand` - Sección de marca
- `.footer-links-section` - Sección de enlaces
- `.social-links-modern` - Contenedor de redes sociales
- `.social-link` - Enlace individual de red social

### Animaciones
- **Hover effects** en enlaces sociales
- **Transiciones suaves** en todos los elementos
- **Animaciones flotantes** en elementos decorativos
- **Efectos de vidrio** con backdrop-filter

## 📈 Próximas Mejoras

### Funcionalidades Futuras
- **Analytics integration** - Seguimiento de clics
- **Social sharing** - Compartir productos
- **Feed integration** - Mostrar posts recientes
- **QR codes** - Códigos QR para perfiles
- **Bio links** - Páginas de enlace personalizadas

### Mejoras de UX
- **Lazy loading** de iconos
- **Preload hints** para enlaces externos
- **Social proof** con contadores de seguidores
- **A/B testing** para diferentes layouts

## 🐛 Solución de Problemas

### Redes sociales no aparecen
1. Verificar que estén marcadas como **activas**
2. Comprobar el **orden** (menor número = mayor prioridad)
3. Revisar que el **context processor** esté registrado
4. Verificar logs de errores en el servidor

### Iconos no se muestran
1. Confirmar que Font Awesome esté cargado
2. Verificar la clase `platform_icon` en el modelo
3. Comprobar que la plataforma esté en la lista soportada

### Footer no es responsive
1. Verificar que los estilos CSS estén cargando
2. Comprobar los media queries
3. Revisar el viewport meta tag

## 📞 Soporte

Para soporte técnico o preguntas sobre la implementación:
- Revisar la documentación del modelo en `home/models.py`
- Ver los estilos en `static/css/styles.css`
- Consultar el administrador en `/admin/home/socialmedia/`

---

**Última actualización**: Noviembre 2024
**Versión**: 1.0.0