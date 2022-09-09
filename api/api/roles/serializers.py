from rest_framework import serializers

from api.clubs.serializers import ClubSerializer

from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'club', 'user', 'assigned_at', 'active']
        extra_kwargs = {'assigned_at': {'read_only': True}}


class ListUserRolesSerializer(serializers.ModelSerializer):
    club = ClubSerializer()

    class Meta:
        model = Role
        fields = ['name', 'club', 'assigned_at', 'active']
        extra_kwargs = {'assigned_at': {'read_only': True}}
