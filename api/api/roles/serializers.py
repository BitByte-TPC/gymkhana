from rest_framework import serializers

from .models import Roles


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['name', 'club', 'user', 'assigned_at', 'active']
