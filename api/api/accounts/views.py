from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from api.roles.serializers import ListUserRolesSerializer

from .permissions import IsOwnerOrAdmin
from .serializers import UserSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """ View to create users """
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    """ View to retrieve and update user """
    permission_classes = (IsOwnerOrAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListUserRoles(generics.ListAPIView):
    """ View to retrieve user roles """
    serializer_class = ListUserRolesSerializer

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id).roles.all()
