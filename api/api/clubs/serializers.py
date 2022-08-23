from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from api.clubs.models import Club, ClubRegistrationRequest


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name', 'category', 'logo', 'description', 'email', 'slug']
        extra_kwargs = {'id': {'read_only': True},
                        'slug': {'read_only': True}
                        }


class ClubRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubRegistrationRequest
        fields = ['id', 'user', 'club', 'fee_submitted', 'status', 'remark', 'updated_at']
        extra_kwargs = {'id': {'read_only': True}, 'user': {
            'read_only': True}, 'club': {'read_only': True}, 'updated_at': {'read_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        club_id = self.context['view'].kwargs.get('pk')
        try:
            club = Club.objects.get(id=club_id)
            return ClubRegistrationRequest.objects.create(user=user, club=club, **validated_data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'detail': 'invalid request'})


class ClubUpdateRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubRegistrationRequest
        fields = ['id', 'user', 'club', 'fee_submitted',
                  'status', 'remark', 'updated_by', 'updated_at']
        extra_kwargs = {'id': {'read_only': True}, 'user': {'read_only': True},
                        'club': {'read_only': True}, 'updated_by': {'read_only': True},
                        'updated_at': {'read_only': True}}

    def update(self, instance, validated_data):
        updatable_fields = ['fee_submitted', 'status', 'remark']
        upadted_by = self.context['request'].user
        for field in updatable_fields:
            field_stored_value = getattr(instance, field)
            field_new_value = validated_data.get(field, field_stored_value)
            setattr(instance, field, field_new_value)
        setattr(instance, 'updated_by', upadted_by)
        instance.save()
        return instance
