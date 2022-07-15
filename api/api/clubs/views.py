from rest_framework.generics import ListAPIView

from .models import Club
from .serializers import ClubSerializer


class ListClubsView(ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
