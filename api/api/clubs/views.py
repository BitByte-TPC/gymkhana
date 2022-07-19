from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser

from .models import Club
from .serializers import ClubSerializer


class ListClubsView(ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class UpdateClubsView(UpdateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
