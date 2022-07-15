from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Club
from .serializers import ClubSerializer


class ListClubsView(ListAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    Response(data=ClubSerializer(queryset, many=True).data)
