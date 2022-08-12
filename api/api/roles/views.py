from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Roles
from .serializers import RolesSerializer


class ListUserRoles(APIView):
    def get(self, request, pk):
        ROLE_COORDINATOR = 'Coordinator'
        ROLE_CO_COORDINATOR = 'Co-Coordinator'
        ROLE_CORE_MEMBER = 'Core member'
        queryset = Roles.objects.filter(
            Q(name__in=[ROLE_COORDINATOR, ROLE_CO_COORDINATOR, ROLE_CORE_MEMBER]) & Q(user=pk))
        if queryset:
            serializer = RolesSerializer(queryset, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
