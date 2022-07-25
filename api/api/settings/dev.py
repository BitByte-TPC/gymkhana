from .settings import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = [  # noqa: F405
    'rest_framework.authentication.SessionAuthentication'
] + REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']  # noqa: F405

LOGGING['root']['level'] = 'DEBUG'  # noqa: F405

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}


ROOT_URLCONF = 'api.dev_urls'
