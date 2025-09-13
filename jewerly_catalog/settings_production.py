"""
Production settings for jewelry catalog application.
This file contains production-specific configurations.
"""
import os
from .settings import *

# Override production settings
DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'yourdomain.com,www.yourdomain.com').split(',')

# Database - Use DATABASE_URL for production (Render standard)
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,  # 10 minutes
            ssl_require=True
        )
    }
else:
    # Fallback for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'jewelry_catalog'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {
                'sslmode': 'require',
            },
            'CONN_MAX_AGE': 600,
        }
    }

# Redis Cache for production
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Email configuration for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Static files served by WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Session and CSRF
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Admin URL (change this for security)
ADMIN_URL = os.getenv('ADMIN_URL', 'admin/')

# Logging for production - Use project directory for logs
LOGGING['handlers']['file']['filename'] = os.path.join(BASE_DIR, 'logs', 'django.log')
LOGGING['handlers']['error_file']['filename'] = os.path.join(BASE_DIR, 'logs', 'errors.log')
LOGGING['handlers']['performance_file']['filename'] = os.path.join(BASE_DIR, 'logs', 'performance.log')
LOGGING['handlers']['security_file']['filename'] = os.path.join(BASE_DIR, 'logs', 'security.log')

# Performance monitoring
MIDDLEWARE.insert(0, 'django.middleware.gzip.GZipMiddleware')

# CORS settings (if using django-cors-headers)
# CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
# CORS_ALLOW_CREDENTIALS = True

# Rate limiting (if using django-ratelimit)
# INSTALLED_APPS.append('django_ratelimit')
# RATELIMIT_RATE = '1000/h'
# RATELIMIT_BLOCK = True

# Monitoring (if using django-prometheus)
# INSTALLED_APPS.append('django_prometheus')
# MIDDLEWARE.insert(0, 'django_prometheus.middleware.PrometheusBeforeMiddleware')
# MIDDLEWARE.append('django_prometheus.middleware.PrometheusAfterMiddleware')

# AWS S3 Configuration for Media Files
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', 'management360')  # Default bucket name
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-2')

# S3 Configuration
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Updated S3 settings for better compatibility and security
AWS_DEFAULT_ACL = None  # Remove default ACL to use bucket policy instead
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Additional S3 settings for better compatibility
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_VERIFY = True

# Use S3 for media files (only if credentials are available)
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    print(f"[S3] Configuring S3 storage with bucket: {AWS_STORAGE_BUCKET_NAME}")
    print(f"[S3] AWS_ACCESS_KEY_ID configured: {'Yes' if AWS_ACCESS_KEY_ID else 'No'}")
    print(f"[S3] AWS_SECRET_ACCESS_KEY configured: {'Yes' if AWS_SECRET_ACCESS_KEY else 'No'}")

    # Use standard S3 storage (compatible with django-storages 1.14.4)
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

else:
    print("[S3] S3 credentials not found, using local storage")
    # Fallback to local storage if S3 is not configured
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Optional: Configure static files on S3 (if needed)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'