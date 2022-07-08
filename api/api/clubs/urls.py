from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListClubsView.as_view())
]
