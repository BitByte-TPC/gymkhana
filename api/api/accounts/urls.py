from django.urls import path

from . import views

urlpatterns = [
  path('', views.UsersListView.as_view()),
]
