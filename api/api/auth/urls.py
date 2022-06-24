from django.urls import path

from .views import TokenView

urlpatterns = [
    path('token/', TokenView.as_view()),
]
