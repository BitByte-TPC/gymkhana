from rest_framework import serializers

from api.clubs.models import Club


class ClubsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['name', 'category', 'logo']
