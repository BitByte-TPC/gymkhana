from django.urls import path

from . import views

urlpatterns = [
    path('', views.CreateUserView.as_view()),
    path('<int:pk>/', views.RetrieveUpdateUserView.as_view()),
    path('accounts/me/roles/', views.ListUserRoles.as_view()),
]
