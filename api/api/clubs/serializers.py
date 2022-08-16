from rest_framework import serializers

from api.clubs.models import Club, ClubRegistrationRequests


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name', 'category', 'logo', 'description', 'email']
        extra_kwargs = {'id': {'read_only': True}}


class ClubRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubRegistrationRequests
        fields = ['id', 'user', 'club', 'fee_submitted', 'status', 'remark', 'updated_by']
        extra_kwargs = {'id': {'read_only': True}}

    def update(self, instance, validated_data):
        updatable_fields = ['fee_submitted', 'status', 'remark', 'updated_by']

        for field in updatable_fields:
            field_stored_value = getattr(instance, field)
            field_new_value = validated_data.get(field, field_stored_value)
            setattr(instance, field, field_new_value)

        instance.save()
        return instance
