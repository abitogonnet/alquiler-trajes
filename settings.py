import os
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta que debería estar en variable de entorno para seguridad
SECRET_KEY = os.environ.get('SECRET_KEY', 'tu-clave-secreta-por-defecto')

# Modo debug, basado en variable de entorno, True de forma local, False en producción
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Hosts permitidos (ajusta para producción con tu dominio o IP)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'prendas',
    'alquileres',
    'gastos',
    'reportes',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL raíz
ROOT_URLCONF = 'alquiler_trajes.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'alquiler_trajes.wsgi.application'

# Base de datos configurada desde variable de entorno DATABASE_URL, con fallback a sqlite local
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}

# Validadores de password
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionalización
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuración estática (muy importante para collectstatic)
STATIC_URL = '/static/'

# Aquí se indica el directorio donde collectstatic copiará los archivos estáticos de la app
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración para archivos estáticos adicionales (opcional)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Tipo de campo por defecto para claves primarias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'