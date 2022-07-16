from django.contrib import admin
from django.urls import include, path

from api.urls import urlpatterns

urlpatterns += [
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
