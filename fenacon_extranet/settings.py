import os
import socket
from decouple import config

SECRET_KEY = config('SECRET_KEY')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (os.path.join(MEDIA_ROOT, 'static'),)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
ADMINS = (
    ('Erivanio Vasconcelos', 'erivanio@cafeepixel.com.br')
)

MANAGERS = ADMINS

DEBUG = config('DEBUG')

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'fenacon_extranet.context_processor.statics',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'easy_thumbnails',
    'image_cropping',
    'widget_tweaks',
    'ckeditor',
    'annoying',
    'localflavor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'selectable',
    'apps.core',
    'apps.financier',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fenacon_extranet.urls'

WSGI_APPLICATION = 'fenacon_extranet.wsgi.application'

AUTH_USER_MODEL = 'core.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', cast=int),
    }
}

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PWD')
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX')
EMAIL_USE_TLS = config('EMAIL_TLS', cast=bool)
EMAIL_PORT = config('EMAIL_PORT', cast=int)


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CKEDITOR_UPLOAD_PATH = 'uploads/ckeditor'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            {'name': 'clipboard',  'items': ['Undo', 'Redo']},
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'RemoveFormat']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent']},
            {'name': 'tools', 'items': ['Maximize']}
        ],
    },
}

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}