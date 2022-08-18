from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView

from .models import Club, ClubRegistrationRequest
from .permissions import IsCoreMemberOrAdmin, IsPositionHolderOrAdmin
from .serializers import ClubRegistrationRequestSerializer, ClubSerializer


class ListClubsView(ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class UpdateClubsView(UpdateAPIView):
    permission_classes = (IsPositionHolderOrAdmin,)
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class CreateClubRegistrationRequestView(CreateAPIView):
    queryset = ClubRegistrationRequest.objects.all()
    serializer_class = ClubRegistrationRequestSerializer


class UpdateClubRegistrationRequestView(UpdateAPIView):
    permission_classes = (IsCoreMemberOrAdmin,)
    queryset = ClubRegistrationRequest.objects.all()
    serializer_class = ClubRegistrationRequestSerializer
