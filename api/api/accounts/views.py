from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from api.roles.models import Roles
from api.roles.serializers import RoleSerializer

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
    """ View to retrieve user roles where user is a core member of a club """
    serializer_class = RoleSerializer
    """User id parameter passed as pk to retrieve user roles """
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        user_roles = User.objects.get(pk=pk).roles.filter(
            name__in=[Roles.ROLE_COORDINATOR, Roles.ROLE_CO_COORDINATOR, Roles.ROLE_CORE_MEMBER])
        return user_roles
