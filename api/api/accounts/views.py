from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer


class UsersListView(generics.CreateAPIView):
    """ View to create users """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
