import uuid

from django.conf import settings
from django.db import models


class Token(models.Model):
    token = models.CharField(max_length=30)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='token', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def find_or_create(user):
        token = Token.objects.filter(user=user).first()
        if not token:
            return Token.objects.create(token=uuid.uuid4().hex, user=user)
        return token
