from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from .models import Role
from .serializers import RoleSerializer


class CreateRoleView(CreateAPIView):
    """ View to create roles """
    permission_classes = (IsAdminUser,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
