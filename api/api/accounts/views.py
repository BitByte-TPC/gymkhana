from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.roles.models import Roles
from api.roles.serializers import RolesSerializer

from .permissions import IsOwnerOrAdmin
from .serializers import UserSerializer

User = get_user_model()


class CreateUserView(CreateAPIView):
    """ View to create users """
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    """ View to retrieve and update user """
    permission_classes = (IsOwnerOrAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListUserRoles(APIView):
    def get(self, request, pk):
        queryset = User.objects.get(pk=pk).roles.filter(
            name__in=[Roles.ROLE_COORDINATOR, Roles.ROLE_CO_COORDINATOR, Roles.ROLE_CORE_MEMBER])
        if queryset:
            serializer = RolesSerializer(queryset, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT, data={})
