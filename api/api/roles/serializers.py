from rest_framework import serializers

from api.clubs.serializers import ClubSerializer
from api.roles.models import Roles


class RolesSerializer(serializers.ModelSerializer):
    club = ClubSerializer(read_only=True)

    class Meta:
        model = Roles
        fields = ['name', 'club', 'assigned_at', 'active']
