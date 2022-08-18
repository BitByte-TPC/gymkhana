from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api.roles.models import Role

from .models import Events
from .permissions import IsCoreMemberOrAdminElseReadOnly
from .serializers import EventSerializer


class ListCreateEventsView(ListCreateAPIView):
    """ View to list and create events """
    queryset = Events.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        if self._has_create_permission(serializer.validated_data):
            serializer.save()
        else:
            raise PermissionDenied({'message': 'You are not allowed to perform this action'})

    # Allow only Core members (including Coordinator and Co-Coordinator)
    # and admins to create events
    def _has_create_permission(self, validated_data):
        allowed_roles = validated_data['club'].roles.filter(
                        Q(name=Role.ROLE_CORE_MEMBER) |
                        Q(name=Role.ROLE_COORDINATOR) |
                        Q(name=Role.ROLE_CO_COORDINATOR))
        user_roles = self.request.user.roles.filter(club__id=validated_data['club'].id)

        return (self.request.user.is_staff or (allowed_roles & user_roles).exists())


class RetrieveUpdateDestroyEventsView(RetrieveUpdateDestroyAPIView):
    """ View to retrieve, update and destroy events """
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsCoreMemberOrAdminElseReadOnly,)
