from django.urls import include, path, re_path

from .views import ping_handler

urlpatterns = [
    path('ping/', ping_handler, name='ping'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
]
