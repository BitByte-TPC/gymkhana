from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListCreateEventsView.as_view()),
]
