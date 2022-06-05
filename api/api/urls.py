from django.urls import path

from .views import ping_handler

urlpatterns = [
    path('ping/', ping_handler, name='ping'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
