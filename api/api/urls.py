from django.urls import path,re_path
from django.urls.conf import include
from django.contrib import admin
from .views import ping_handler
import os

urlpatterns = [
    
    path('ping/', ping_handler, name='ping'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')), 
]

if os.environ.get('ENV')=='dev':
    urlpatterns.append(path('admin/',admin.site.urls))