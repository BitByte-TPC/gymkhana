from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListCreateEventsView.as_view()),
    path('<int:pk>/', views.RetrieveUpdateDestroyEventsView.as_view()),
]
