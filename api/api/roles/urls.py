from django.urls import path

from . import views

urlpatterns = [
    path('', views.CreateRoleView.as_view()),
]
