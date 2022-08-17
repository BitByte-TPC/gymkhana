from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListClubsView.as_view()),
    path('<int:pk>/', views.UpdateClubsView.as_view()),
    path('registration/', views.CreateClubRegistrationRequestView.as_view()),
    path('registration/<int:pk>/', views.UpdateClubRegistrationRequestView.as_view())
]
