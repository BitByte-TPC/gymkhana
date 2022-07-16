from django.urls import path
from django.urls.conf import include

from .views import ping_handler

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('clubs/', include('api.clubs.urls')),
    path('ping/', ping_handler, name='ping'),
    path('users/', include('api.accounts.urls')),
]
