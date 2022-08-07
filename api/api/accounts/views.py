from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .permissions import IsOwnerOrAdmin
from .serializers import UserSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """ View to create users """
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    """ View to update user """
    permission_classes = (IsOwnerOrAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
