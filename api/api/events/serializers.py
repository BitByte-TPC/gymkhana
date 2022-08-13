from api.events.models import Events
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'name', 'description', 'starts_at', 'ends_at', 'registration_required',
                  'created_by', 'image_url', 'club', 'registration_approval_required', 'address']
        extra_kwargs = {'id': {'read_only': True}}
