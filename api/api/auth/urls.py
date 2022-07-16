from django.urls import path

from .views import DeleteTokenView, TokenView

urlpatterns = [
    path('token/', TokenView.as_view()),
    path('token:revoke/', DeleteTokenView.as_view())
]
