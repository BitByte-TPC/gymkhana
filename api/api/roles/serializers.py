from rest_framework import serializers

from api.clubs.serializers import ClubSerializer
from api.roles.models import Roles


class RoleSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Roles
        fields = ['name', 'club', 'assigned_at', 'active']
        extra_kwargs = {'assigned_at': {'read_only': True}}
