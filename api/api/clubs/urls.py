from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListClubsView.as_view()),
    path('<int:pk>/', views.UpdateClubsView.as_view()),
    path('<int:pk>/registration-requests/', views.CreateClubRegistrationRequestView.as_view()),
    path('<int:club_id>/registration-requests/<int:registration_id>/',
         views.UpdateClubRegistrationRequestView.as_view())
]
