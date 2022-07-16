import os

from .settings import *  # noqa: F403, F401

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ['rest_framework.renderers.JSONRenderer']  # noqa: F405

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_POSTGRES_NAME'),
        'USER': os.environ.get('DB_POSTGRES_USER'),
        'PASSWORD': os.environ.get('DB_POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_POSTGRES_HOST'),
        'PORT': os.environ.get('DB_POSTGRES_PORT'),
    }
}
