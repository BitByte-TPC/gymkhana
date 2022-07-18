from django.urls import path

from . import views

urlpatterns = [
  path('', views.CreateUserView.as_view()),
  path('<int:pk>/', views.UpdateUserView.as_view()),
]
