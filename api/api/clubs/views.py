from rest_framework.generics import ListAPIView, UpdateAPIView

from .models import Club
from .permissions import IsPositionHolderOrAdmin
from .serializers import ClubSerializer


class ListClubsView(ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class UpdateClubsView(UpdateAPIView):
    permission_classes = (IsPositionHolderOrAdmin,)
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
