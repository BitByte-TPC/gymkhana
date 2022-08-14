from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

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
        ROLE_COORDINATOR = 'Coordinator'
        ROLE_CO_COORDINATOR = 'Co-Coordinator'
        ROLE_CORE_MEMBER = 'Core member'

        queryset = User.objects.get(pk=pk).roles.all().filter(
            name__in=[ROLE_COORDINATOR, ROLE_CO_COORDINATOR, ROLE_CORE_MEMBER])
        if queryset:
            serializer = RolesSerializer(queryset, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
