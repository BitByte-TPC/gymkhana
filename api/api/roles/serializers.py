from rest_framework import serializers

from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'club', 'user', 'assigned_at', 'active']
        extra_kwargs = {'assigned_at': {'read_only': True}}
