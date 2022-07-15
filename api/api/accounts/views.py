from rest_framework import generics

from .models import User
from .serializers import UserSerializer


class UsersListView(generics.CreateAPIView):
    """ View to create users """
    queryset = User.objects.all()
    serializer_class = UserSerializer
