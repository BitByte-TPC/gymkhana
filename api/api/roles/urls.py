from django.urls import path

from . import views

urlpatterns = [
    path('', views.CreateRolesView.as_view()),
]
