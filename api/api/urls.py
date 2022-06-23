import os

from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from .views import ping_handler

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('api.auth.urls')),
    path('ping/', ping_handler, name='ping'),
]

if os.environ.get('ENV') == 'dev':
    urlpatterns.append(path('admin/', admin.site.urls))
