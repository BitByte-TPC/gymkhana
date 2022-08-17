from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from .models import Roles
from .serializers import RolesSerializer


class CreateRolesView(CreateAPIView):
    """ View to create roles """
    permission_classes = (IsAdminUser,)
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
