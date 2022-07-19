from rest_framework import serializers

from api.clubs.models import Club


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name', 'category', 'logo', 'description', 'email']
        extra_kwargs = {'id': {'read_only': True},
                        'description': {'write_only': True},
                        'email': {'write_only': True}
                        }
